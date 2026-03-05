# blockchain/algorand_deploy.py
"""Algorand blockchain interaction utilities for RANZR."""

import os
from algosdk.v2client import algod
from algosdk import transaction, account, mnemonic
from config import settings

def get_algod_client():
    """Initializes and returns an Algod client connected to TestNet."""
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    headers = {"X-Algo-API-Token": algod_token}
    return algod.AlgodClient(algod_token, algod_address, headers)

def log_incident_to_algorand(incident_hash: str) -> str:
    """
    Logs an incident hash to the Algorand TestNet as a transaction note.
    Uses 'algorand_mnemonic' from config or environment variables if available.
    """
    sender_mnemonic = settings.get("algorand_mnemonic") or os.environ.get("ALGORAND_MNEMONIC")

    if not sender_mnemonic:
        print(" -> Warning: No Algorand mnemonic provided in config.")
        print(" -> [Simulated Algorand Transaction]: Simulating blockchain logging offline...")
        print(f" -> Prepared incident hash for future deployment: {incident_hash}")
        status_msg = "Simulated Blockchain Tx (config pending)"
        # Simulate txid
        import hashlib
        simulated_txid = hashlib.sha256(incident_hash.encode()).hexdigest()[:16].upper()
        return simulated_txid

    # If mnemonic is provided, attempt actual transaction
    try:
        private_key = mnemonic.to_private_key(sender_mnemonic)
        sender_address = account.address_from_private_key(private_key)
        
        client = get_algod_client()
        params = client.suggested_params()
        
        note = incident_hash.encode()
        
        # 0 ALGO transaction to oneself to store the note
        unsigned_txn = transaction.PaymentTxn(
            sender=sender_address,
            sp=params,
            receiver=sender_address,
            amt=0,
            note=note
        )
        
        # Sign the transaction
        signed_txn = unsigned_txn.sign(private_key)
        
        # Submit the transaction
        txid = client.send_transaction(signed_txn)
        print(f" -> Successfully sent Algorand transaction with TxID: {txid}")
        return txid
    except Exception as e:
        print(f" -> Failed to submit transaction to Algorand TestNet: {e}")
        return None
