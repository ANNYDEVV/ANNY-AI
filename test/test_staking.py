import unittest
from app.staking_dashboard.staking_api import app, db, Staker
from flask import json

class TestStakingAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client and database for testing."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_staking.db'
        app.config['TESTING'] = True
        cls.client = app.test_client()

        # Initialize the database
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database after all tests are run."""
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Set up the test database with sample data before each test."""
        self.sample_staker_1 = Staker(address="0xABC123", staked_amount=100.0, rewards=0.0)
        self.sample_staker_2 = Staker(address="0xDEF456", staked_amount=200.0, rewards=0.0)

        db.session.add(self.sample_staker_1)
        db.session.add(self.sample_staker_2)
        db.session.commit()

    def tearDown(self):
        """Clear the database after each test."""
        db.session.query(Staker).delete()
        db.session.commit()

    def test_stake_tokens(self):
        """Test the staking endpoint."""
        response = self.client.post('/stake', json={"address": "0xNEW123", "amount": 50.0})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully staked", data["message"])
        self.assertEqual(data["staked_amount"], 50.0)

    def test_unstake_tokens(self):
        """Test the unstaking endpoint."""
        response = self.client.post('/unstake', json={"address": "0xABC123", "amount": 50.0})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully unstaked", data["message"])
        self.assertEqual(data["staked_amount"], 50.0)

    def test_unstake_insufficient_balance(self):
        """Test the unstaking endpoint with insufficient balance."""
        response = self.client.post('/unstake', json={"address": "0xABC123", "amount": 150.0})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Insufficient staked balance", data["error"])

    def test_list_stakers(self):
        """Test the endpoint to list all stakers."""
        response = self.client.get('/stakers')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["address"], "0xABC123")
        self.assertEqual(data[1]["address"], "0xDEF456")

    def test_distribute_rewards(self):
        """Test the reward distribution endpoint."""
        response = self.client.post('/distribute_rewards', json={"total_rewards": 300.0})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Rewards distributed successfully", data["message"])

        staker_1 = Staker.query.filter_by(address="0xABC123").first()
        staker_2 = Staker.query.filter_by(address="0xDEF456").first()

        self.assertAlmostEqual(staker_1.rewards, 100.0, places=2)
        self.assertAlmostEqual(staker_2.rewards, 200.0, places=2)

if __name__ == "__main__":
    unittest.main()
