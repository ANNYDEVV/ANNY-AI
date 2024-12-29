import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Config
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Solana Config
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")

# General Config
TRADE_AMOUNT_SOL = float(os.getenv("TRADE_AMOUNT_SOL", 0.01))  # Default to 0.01 SOL

# Database Config
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")
