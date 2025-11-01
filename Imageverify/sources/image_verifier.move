// file: sources/image_verifier.move
//
// This module is the "truth ledger" for our deepfake detection.
// It's designed to be published under a specific account, which
// we call 'verifier_admin'.
//
module verifier_admin::image_verifier {

    use std::signer;
    use std::vector;
    use aptos_framework::table::{Self, Table};
    use aptos_framework::timestamp;

    /// Error: The image hash already has a verdict.
    const E_VERDICT_ALREADY_EXISTS: u64 = 1;
    /// Error: The admin hasn't run the initialize_module function yet.
    const E_STORE_NOT_PUBLISHED: u64 = 2;

    /// This struct holds the on-chain verification result.
    struct ImageVerdict has store, key, drop {
        /// The SHA-256 hash of the image file.
        image_hash: vector<u8>,
        /// The AI model's verdict.
        is_deepfake: bool,
        /// The AI model's confidence (e.g., 95 for 95%).
        confidence_score: u8,
        /// The address of the trusted server (oracle) that ran the AI.
        verified_by: address,
        /// The on-chain timestamp of when this was recorded.
        verified_at: u64,
    }

    /// This resource holds the master Table of all verdicts.
    /// It is stored under the 'verifier_admin' account.
    struct VerdictStore has key {
        /// The table mapping an image's hash (vector<u8>) to its ImageVerdict.
        verdicts: Table<vector<u8>, ImageVerdict>,
    }

    /// --- Initialization Function ---
    /// The admin account MUST call this *once* after publishing
    /// to create the VerdictStore.
    public entry fun initialize_module(admin: &signer) {
        let admin_addr = signer::address_of(admin);

        // Assert the store doesn't already exist.
        assert!(!exists<VerdictStore>(admin_addr), E_STORE_NOT_PUBLISHED);

        // Create and move the VerdictStore resource to the admin's account.
        move_to(admin, VerdictStore {
            verdicts: table::new(),
        });
    }

    /// --- Entry Function (Called by our Python Server) ---
    /// This function is called by our trusted off-chain AI server (the "oracle")
    /// to permanently register a new image's verdict.
    public entry fun register_verdict(
        oracle: &signer,
        image_hash: vector<u8>,
        is_fake: bool,
        confidence: u8
    ) acquires VerdictStore {
        let oracle_addr = signer::address_of(oracle);

        // We assume the module is published at '@verifier_admin'
        let admin_addr = @verifier_admin; 

        // Ensure the store has been initialized
        assert!(exists<VerdictStore>(admin_addr), E_STORE_NOT_PUBLISHED);

        // Borrow a mutable reference to the store
        let store = borrow_global_mut<VerdictStore>(admin_addr);

        // Ensure we haven't already verified this exact image
        assert!(!table::contains(&store.verdicts, image_hash), E_VERDICT_ALREADY_EXISTS);

        // Create the new verdict struct
        let new_verdict = ImageVerdict {
            image_hash: image_hash,
            is_deepfake: is_fake,
            confidence_score: confidence,
            verified_by: oracle_addr,
            verified_at: timestamp::now_seconds(),
        };

        // Add the new verdict to the table, using its hash as the key
        table::add(&mut store.verdicts, image_hash, new_verdict);
    }

    /// --- View Function (Publicly Readable) ---
    /// Anyone can call this function for free to check the verdict
    /// for a given image hash.
    #[view]
    public fun get_verdict(image_hash: vector<u8>): (bool, u8, address, u64)
    acquires VerdictStore {

        let admin_addr = @verifier_admin;
        assert!(exists<VerdictStore>(admin_addr), E_STORE_NOT_PUBLISHED);

        let store = borrow_global<VerdictStore>(admin_addr);
        assert!(table::contains(&store.verdicts, image_hash), E_VERDICT_ALREADY_EXISTS);

        // Get the verdict from the table
        let verdict = table::borrow(&store.verdicts, image_hash);

        // Return the useful fields
        (
            verdict.is_deepfake,
            verdict.confidence_score,
            verdict.verified_by,
            verdict.verified_at
        )
    }
}