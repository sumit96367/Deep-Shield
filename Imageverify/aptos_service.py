# file: aptos_service.py
import os
import asyncio
from aptos_sdk.account import Account, AccountAddress
from aptos_sdk.async_client import RestClient, ClientConfig
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    SignedTransaction,
    TransactionArgument,
)

# --- ------------------- ---
# --- CRITICAL CONFIG ---
# --- ------------------- ---
# PASTE YOUR MODULE PUBLISHER ADDRESS (from aptos account list)
MODULE_ADDRESS_STR = "0xb090137780fdb6561748c2f099d494d658ce277f44ed6c35ac7e5351c65b259e" 

# PASTE YOUR ACCOUNT PRIVATE KEY (from .aptos/config.yaml)
ORACLE_PRIVATE_KEY_STR = "ed25519-priv-0x20b799e53c18e3ea32996630ceca9da09b37a7a1fd09105ccb196e3c30fd5b52" 
# --- ------------------- ---
# --- ------------------- ---

# --- Constants ---
NODE_URL = "https://fullnode.devnet.aptoslabs.com/v1" # Aptos Devnet

# --- Global Clients (Initialized once) ---
try:
    MODULE_ADDRESS = AccountAddress.from_str_relaxed(MODULE_ADDRESS_STR)
    ORACLE_ACCOUNT = Account.load_key(ORACLE_PRIVATE_KEY_STR)
    CLIENT = RestClient(NODE_URL, ClientConfig())
    print("Aptos Service Loaded.")
    print(f"Connecting to node: {NODE_URL}")
    print(f"Using Oracle Address: {ORACLE_ACCOUNT.address()}")
except Exception as e:
    print(f"ERROR: Failed to initialize Aptos Service. Check your private key and address.")
    print(f"Details: {e}")
    # We exit here because the server can't run without this.
    exit(1)


async def register_verdict_on_chain(image_hash: bytes, is_fake: bool, confidence: int) -> str:
    """
    Submits the AI verdict to the Aptos smart contract.
    Returns the transaction hash.
    """

    # 1. Build the transaction payload using TransactionArgument
    transaction_args = [
        TransactionArgument(image_hash, Serializer.to_bytes),
        TransactionArgument(is_fake, Serializer.bool),
        TransactionArgument(confidence, Serializer.u8),
    ]
    
    payload = EntryFunction.natural(
        f"{MODULE_ADDRESS_STR}::image_verifier", # Module ID
        "register_verdict",                     # Function name
        [],                                     # Type arguments (none for this function)
        transaction_args,
    )

    # 2. Create and submit the signed transaction
    try:
        print("Creating and signing transaction...")
        signed_tx = await CLIENT.create_bcs_signed_transaction(
            ORACLE_ACCOUNT,
            TransactionPayload(payload),
        )
        
        print("Submitting transaction...")
        tx_hash = await CLIENT.submit_bcs_transaction(signed_tx)
        print(f"Transaction submitted with hash: {tx_hash}")

        # Wait for the transaction to be finalized
        await CLIENT.wait_for_transaction(tx_hash) 
        print(f"Transaction finalized!")
        return tx_hash
    except Exception as e:
        print(f"Error submitting transaction: {e}")
        error_str = str(e)
        
        # Extract simple error messages
        if "E_VERDICT_ALREADY_EXISTS" in error_str or "already has a verdict" in error_str:
            raise Exception("This image has already been verified on the blockchain.")
        elif "insufficient balance" in error_str.lower():
            raise Exception("Insufficient balance to complete the transaction.")
        elif "timeout" in error_str.lower():
            raise Exception("Transaction timed out. Please try again.")
        elif "network" in error_str.lower() or "connection" in error_str.lower():
            raise Exception("Network error. Please check your connection and try again.")
        else:
            # For other errors, try to extract a simple message from vm_status if present
            import re
            if "vm_status" in error_str:
                # Try to find "Error: ..." pattern in vm_status
                match = re.search(r'Error:\s*([^"]+)', error_str, re.IGNORECASE)
                if match:
                    message = match.group(1).strip().rstrip('"').rstrip("'")
                    # Clean up any remaining quotes or brackets
                    message = message.split('"')[0].split("'")[0].split('(')[0].strip()
                    if message and len(message) < 150:
                        raise Exception(message)
                # Try to find "already has a verdict" pattern
                if "already has a verdict" in error_str.lower():
                    raise Exception("This image has already been verified on the blockchain.")
            raise Exception("Transaction failed. Please try again.")
    
# file: aptos_service.py
# ... all your other imports and code ...

async def get_verdict_from_chain(image_hash_hex: str) -> dict:
    """
    Calls the 'get_verdict' view function on the smart contract.
    Returns the on-chain data.
    """
    print(f"Checking hash on-chain: {image_hash_hex}")
    
    try:
        # 1. Convert hex string back to raw bytes
        image_hash_bytes = bytes.fromhex(image_hash_hex)
        
        # 2. Define the view function payload
        payload = {
            "function": f"{MODULE_ADDRESS_STR}::image_verifier::get_verdict",
            "type_arguments": [],
            "arguments": [
                Serializer.to_bytes(image_hash_bytes),
            ],
        }

        # 3. Call the view function
        # Note: client.view() is synchronous, so we run it in an executor
        # to avoid blocking the async server.
        # (This is an advanced, but correct, way to handle this)
        import asyncio
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, CLIENT.view, payload)
        
        # 4. Decode the result
        # The result from a view function is a simple JSON list
        # based on our return types: (bool, u8, address, u64)
        is_fake = result[0]
        confidence = result[1]
        verified_by = result[2]
        verified_at = result[3] # This is a Unix timestamp

        # Convert timestamp to a readable string
        from datetime import datetime
        verified_at_str = datetime.fromtimestamp(verified_at).strftime('%Y-%m-%d %H:%M:%S')

        return {
            "found": True,
            "is_deepfake": is_fake,
            "confidence": confidence,
            "verified_by": verified_by,
            "verified_at": verified_at_str
        }

    except Exception as e:
        error_string = str(e)
        # This is the error Aptos throws when a resource is not found
        if "E_VERDICT_ALREADY_EXISTS" in error_string or "Resource not found" in error_string:
             print("Hash not found on chain.")
             return {"found": False}
        
        # Handle other errors
        print(f"Error checking hash: {e}")
        raise e