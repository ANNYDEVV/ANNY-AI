import requests
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.system_program import TransferParams, transfer
import base64
import os

# Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"  # Solana mainnet RPC endpoint
PRIVATE_KEY_PATH = "wallet/private_key.json"  # Path to private key file
DEFAULT_RECEIVER = "ReceiverPublicKeyHere"  # Replace with actual receiver wallet
TRADE_AMOUNT = 0.01  # Amount in SOL to trade

# Initialize Solana client
solana_client = Client(SOLANA_RPC_URL)

# Load private key
def load_private_key():
    if not os.path.exists(PRIVATE_KEY_PATH):
        raise FileNotFoundError("Private key file not found.")

    with open(PRIVATE_KEY_PATH, "r") as key_file:
        private_key_data = key_file.read()
        private_key = base64.b64decode(private_key_data)
        return Keypair.from_secret_key(private_key)

# Check wallet balance
def check_balance(wallet_address):
    response = solana_client.get_balance(wallet_address)
    if "result" in response:
        balance = response["result"]["value"] / 1e9  # Convert lamports to SOL
        return balance
    else:
        raise Exception(f"Failed to fetch balance: {response}")

# Execute trade
def execute_trade(sender_keypair, receiver_address, amount):
    sender_public_key = sender_keypair.public_key
    transaction = Transaction()

    # Create transfer instruction
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=sender_public_key,
            to_pubkey=receiver_address,
            lamports=int(amount * 1e9)  # Convert SOL to lamports
        )
    )

    # Add instruction to transaction
    transaction.add(transfer_instruction)

    # Sign and send transaction
    response = solana_client.send_transaction(
        transaction,
        sender_keypair,
        opts=TxOpts(skip_preflight=True)
    )

    if "result" in response:
        print(f"Transaction successful: {response['result']}\nView on Solana Explorer: https://explorer.solana.com/tx/{response['result']}?cluster=mainnet-beta")
    else:
        print(f"Transaction failed: {response}")

# Main function for trading
def main():
    print("Initializing trading logic...")
    
    # Load private key and check balance
    sender_keypair = load_private_key()
    sender_address = sender_keypair.public_key
    print(f"Loaded wallet: {sender_address}")

    balance = check_balance(sender_address)
    print(f"Wallet balance: {balance:.2f} SOL")

    if balance < TRADE_AMOUNT:
        raise Exception("Insufficient balance for trade.")

    # Execute trade
    print(f"Executing trade: Sending {TRADE_AMOUNT} SOL to {DEFAULT_RECEIVER}...")
    execute_trade(sender_keypair, DEFAULT_RECEIVER, TRADE_AMOUNT)

if __name__ == "__main__":
    main()
