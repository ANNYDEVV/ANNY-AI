import unittest
from app.utils import clean_tweet, validate_address, calculate_reward_share

class TestUtils(unittest.TestCase):

    def test_clean_tweet(self):
        """Test the tweet cleaning functionality."""
        dirty_tweet = "Bitcoin to the moon!!! 🚀🚀 http://example.com"
        expected_cleaned = "bitcoin to the moon"
        cleaned_tweet = clean_tweet(dirty_tweet)
        self.assertEqual(cleaned_tweet, expected_cleaned, "Tweet should be cleaned correctly.")

    def test_clean_tweet_empty(self):
        """Test cleaning an empty tweet."""
        dirty_tweet = ""
        cleaned_tweet = clean_tweet(dirty_tweet)
        self.assertEqual(cleaned_tweet, "", "Empty tweet should remain empty.")

    def test_validate_address_valid(self):
        """Test validating a correct Solana wallet address."""
        valid_address = "8ruvf7BjkyT5GorxWyZ8GvQMaLQ5x1FvTrm9XAtLgSHZ"
        self.assertTrue(validate_address(valid_address), "Valid address should return True.")

    def test_validate_address_invalid(self):
        """Test validating an incorrect Solana wallet address."""
        invalid_address = "InvalidAddress123"
        self.assertFalse(validate_address(invalid_address), "Invalid address should return False.")

    def test_calculate_reward_share(self):
        """Test calculating reward shares for stakers."""
        staked_amounts = [100, 200, 300]
        total_rewards = 600
        expected_shares = [100, 200, 300]
        calculated_shares = calculate_reward_share(staked_amounts, total_rewards)
        self.assertEqual(calculated_shares, expected_shares, "Reward shares should match expected values.")

    def test_calculate_reward_share_zero_total(self):
        """Test calculating reward shares with zero total rewards."""
        staked_amounts = [100, 200, 300]
        total_rewards = 0
        expected_shares = [0, 0, 0]
        calculated_shares = calculate_reward_share(staked_amounts, total_rewards)
        self.assertEqual(calculated_shares, expected_shares, "All shares should be zero if total rewards are zero.")

    def test_calculate_reward_share_empty(self):
        """Test calculating reward shares with no stakers."""
        staked_amounts = []
        total_rewards = 600
        expected_shares = []
        calculated_shares = calculate_reward_share(staked_amounts, total_rewards)
        self.assertEqual(calculated_shares, expected_shares, "Shares should be empty if there are no stakers.")

if __name__ == "__main__":
    unittest.main()
