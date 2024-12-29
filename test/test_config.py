import unittest
import os
from app.config.config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, SOLANA_RPC_URL, TRADE_AMOUNT_SOL, DATABASE_URI

class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up environment variables for testing."""
        os.environ["TWITTER_API_KEY"] = "test_api_key"
        os.environ["TWITTER_API_SECRET"] = "test_api_secret"
        os.environ["TWITTER_ACCESS_TOKEN"] = "test_access_token"
        os.environ["TWITTER_ACCESS_SECRET"] = "test_access_secret"
        os.environ["SOLANA_RPC_URL"] = "https://api.testnet.solana.com"
        os.environ["TRADE_AMOUNT_SOL"] = "0.01"
        os.environ["DATABASE_URI"] = "sqlite:///test_app.db"

    def test_twitter_api_config(self):
        """Test that Twitter API configurations are loaded correctly."""
        self.assertEqual(TWITTER_API_KEY, "test_api_key", "Twitter API Key should match environment variable.")
        self.assertEqual(TWITTER_API_SECRET, "test_api_secret", "Twitter API Secret should match environment variable.")
        self.assertEqual(TWITTER_ACCESS_TOKEN, "test_access_token", "Twitter Access Token should match environment variable.")
        self.assertEqual(TWITTER_ACCESS_SECRET, "test_access_secret", "Twitter Access Secret should match environment variable.")

    def test_solana_rpc_url(self):
        """Test that the Solana RPC URL is loaded correctly."""
        self.assertEqual(SOLANA_RPC_URL, "https://api.testnet.solana.com", "Solana RPC URL should match environment variable.")

    def test_trade_amount(self):
        """Test that the trade amount in SOL is loaded correctly."""
        self.assertEqual(TRADE_AMOUNT_SOL, 0.01, "Trade amount should match environment variable and default to 0.01.")

    def test_database_uri(self):
        """Test that the database URI is loaded correctly."""
        self.assertEqual(DATABASE_URI, "sqlite:///test_app.db", "Database URI should match environment variable.")

    @classmethod
    def tearDownClass(cls):
        """Clean up environment variables after tests."""
        del os.environ["TWITTER_API_KEY"]
        del os.environ["TWITTER_API_SECRET"]
        del os.environ["TWITTER_ACCESS_TOKEN"]
        del os.environ["TWITTER_ACCESS_SECRET"]
        del os.environ["SOLANA_RPC_URL"]
        del os.environ["TRADE_AMOUNT_SOL"]
        del os.environ["DATABASE_URI"]

if __name__ == "__main__":
    unittest.main()
