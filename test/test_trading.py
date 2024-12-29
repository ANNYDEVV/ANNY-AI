import unittest
from unittest.mock import patch, MagicMock
from app.trading_logic.trade_execution import execute_trade
from solana.keypair import Keypair
from solana.rpc.api import Client

class TestTradingLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up necessary resources for testing."""
        cls.mock_keypair = Keypair.from_secret_key(bytes([1] * 64))  # Mock keypair for testing
        cls.receiver_address = "8ruvf7BjkyT5GorxWyZ8GvQMaLQ5x1FvTrm9XAtLgSHZ"
        cls.trade_amount = 0.01  # Amount in SOL to trade
        cls.solana_client = Client("https://api.mainnet-beta.solana.com")

    @patch("app.trading_logic.trade_execution.Client")
    def test_execute_trade_success(self, mock_client):
        """Test a successful trade execution."""
        # Mock Solana client response
        mock_client.return_value.send_transaction.return_value = {
            "result": "mock_transaction_signature"
        }

        response = execute_trade(self.mock_keypair, self.receiver_address, self.trade_amount)

        self.assertIn("mock_transaction_signature", response)
        self.assertIn("Trade executed successfully", response)

    @patch("app.trading_logic.trade_execution.Client")
    def test_execute_trade_insufficient_balance(self, mock_client):
        """Test trade execution with insufficient balance."""
        # Mock Solana client response for insufficient funds
        mock_client.return_value.send_transaction.side_effect = Exception("Insufficient funds")

        with self.assertRaises(Exception) as context:
            execute_trade(self.mock_keypair, self.receiver_address, self.trade_amount)

        self.assertIn("Insufficient funds", str(context.exception))

    @patch("app.trading_logic.trade_execution.Client")
    def test_execute_trade_invalid_address(self, mock_client):
        """Test trade execution with an invalid receiver address."""
        invalid_address = "InvalidAddress123"

        with self.assertRaises(Exception) as context:
            execute_trade(self.mock_keypair, invalid_address, self.trade_amount)

        self.assertIn("Invalid address", str(context.exception))

    @patch("app.trading_logic.trade_execution.Client")
    def test_execute_trade_network_error(self, mock_client):
        """Test trade execution with a network error."""
        mock_client.return_value.send_transaction.side_effect = Exception("Network error")

        with self.assertRaises(Exception) as context:
            execute_trade(self.mock_keypair, self.receiver_address, self.trade_amount)

        self.assertIn("Network error", str(context.exception))

if __name__ == "__main__":
    unittest.main()
