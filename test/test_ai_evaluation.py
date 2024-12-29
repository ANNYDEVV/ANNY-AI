import unittest
from app.ai_evaluation.tweet_analysis import analyze_tweets, clean_tweet, build_ai_pipeline, train_pipeline
from textblob import TextBlob
import os
import joblib

class TestAIEvaluation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup resources for all test cases."""
        cls.sample_tweets = [
            "Bitcoin is the best investment!",
            "Crypto is a scam, don't invest!",
            "Ethereum will outperform Bitcoin.",
        ]
        cls.labels = [1, 0, 1]  # 1 for positive, 0 for negative sentiment

        # Ensure any previously saved pipeline is removed for clean testing
        if os.path.exists("ai_pipeline.pkl"):
            os.remove("ai_pipeline.pkl")

    def test_clean_tweet(self):
        """Test the tweet cleaning functionality."""
        dirty_tweet = "Bitcoin to the moon!!! 🚀🚀 http://example.com"
        expected_cleaned = "bitcoin to the moon"
        self.assertEqual(clean_tweet(dirty_tweet), expected_cleaned)

    def test_sentiment_analysis(self):
        """Test sentiment analysis using TextBlob."""
        tweet = "Bitcoin is amazing!"
        polarity = TextBlob(tweet).sentiment.polarity
        self.assertGreater(polarity, 0, "Expected positive sentiment.")

    def test_build_ai_pipeline(self):
        """Test if the AI pipeline is built successfully."""
        pipeline = build_ai_pipeline()
        self.assertIsNotNone(pipeline, "Pipeline should not be None.")

    def test_train_and_save_pipeline(self):
        """Test training and saving the AI pipeline."""
        pipeline = build_ai_pipeline()
        train_pipeline(pipeline, self.sample_tweets, self.labels)

        # Check if the model file is saved
        self.assertTrue(os.path.exists("ai_pipeline.pkl"), "Pipeline file should exist.")

    def test_load_pipeline(self):
        """Test loading the trained AI pipeline."""
        if not os.path.exists("ai_pipeline.pkl"):
            pipeline = build_ai_pipeline()
            train_pipeline(pipeline, self.sample_tweets, self.labels)

        loaded_pipeline = joblib.load("ai_pipeline.pkl")
        self.assertIsNotNone(loaded_pipeline, "Loaded pipeline should not be None.")

    def test_tweet_evaluation(self):
        """Test tweet evaluation with the trained pipeline."""
        pipeline = build_ai_pipeline()
        train_pipeline(pipeline, self.sample_tweets, self.labels)

        # Use the trained pipeline for prediction
        predictions = pipeline.predict([clean_tweet(tweet) for tweet in self.sample_tweets])
        self.assertEqual(predictions.tolist(), self.labels, "Predictions should match the labels.")

    @classmethod
    def tearDownClass(cls):
        """Cleanup resources after all tests."""
        if os.path.exists("ai_pipeline.pkl"):
            os.remove("ai_pipeline.pkl")

if __name__ == "__main__":
    unittest.main()
