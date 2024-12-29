import requests
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import transfer
from solana.rpc.types import TxOpts
import time
import json
import os

# Solana RPC Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
TRADE_AMOUNT = 0.01  # Amount in SOL per trade

# Path to Keypair JSON
KEYPAIR_PATH = "bot_keypair.json"

# Initialize Solana Client
solana_client = Client(SOLANA_RPC_URL)

# Load Solana Keypair
def load_keypair():
    if not os.path.exists(KEYPAIR_PATH):
        raise FileNotFoundError(f"Keypair file not found at {KEYPAIR_PATH}")

    with open(KEYPAIR_PATH, "r") as keypair_file:
        keypair_data = json.load(keypair_file)
        return Keypair.from_secret_key(bytes(keypair_data))

# Fetch Memecoin Market Data (Dummy Endpoint)
def fetch_memecoin_data():
    try:
        response = requests.get("https://api.example.com/memecoins")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching memecoin data: {e}")
        return []

# Evaluate and Choose Memecoin
def evaluate_memecoin(memecoins):
    # Dummy logic: Choose the coin with highest "hype_score"
    sorted_memecoins = sorted(memecoins, key=lambda x: x.get("hype_score", 0), reverse=True)
    return sorted_memecoins[0] if sorted_memecoins else None

# Execute Trade on Solana Blockchain
def execute_trade(keypair, receiver_address, amount):
    transaction = Transaction()
    transaction.add(
        transfer(
            TransferParams(
                from_pubkey=keypair.public_key,
                to_pubkey=receiver_address,
                lamports=int(amount * 1e9)  # Convert SOL to lamports
            )
        )
    )

    try:
        response = solana_client.send_transaction(
            transaction, keypair, opts=TxOpts(skip_preflight=True)
        )
        if "result" in response:
            print(f"Trade executed successfully: {response['result']}\nView on Solana Explorer: https://explorer.solana.com/tx/{response['result']}?cluster=mainnet-beta")
        else:
            print(f"Trade failed: {response}")
    except Exception as e:
        print(f"Error executing trade: {e}")

# Bot Main Loop
def trading_bot():
    keypair = load_keypair()
    print(f"Bot initialized with public key: {keypair.public_key}")

    while True:
        print("Fetching memecoin data...")
        memecoins = fetch_memecoin_data()

        if not memecoins:
            print("No memecoins data available. Retrying in 60 seconds...")
            time.sleep(60)
            continue

        memecoin = evaluate_memecoin(memecoins)
        if not memecoin:
            print("No suitable memecoin found. Retrying in 60 seconds...")
            time.sleep(60)
            continue

        print(f"Selected memecoin: {memecoin['name']} (Hype Score: {memecoin['hype_score']})")
        receiver_address = memecoin['address']

        print(f"Executing trade: Sending {TRADE_AMOUNT} SOL to {receiver_address}...")
        execute_trade(keypair, receiver_address, TRADE_AMOUNT)

        print("Trade complete. Retrying in 300 seconds...")
        time.sleep(300)

if __name__ == "__main__":
    trading_bot()
