import tweepy
import re
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Configuration for Twitter API (Replace with your keys and tokens)
TWITTER_API_KEY = "your_api_key"
TWITTER_API_SECRET = "your_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# Authenticate Twitter API
def authenticate_twitter():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)

# Preprocessing tweets
def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'[^a-zA-Z ]', '', tweet)  # Remove non-alphabetic characters
    tweet = tweet.lower()  # Convert to lowercase
    return tweet

# Analyze tweet sentiment using TextBlob
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity

# Collect tweets by hashtag
def collect_tweets(api, hashtag, count=100):
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, lang="en", tweet_mode="extended").items(count):
            if hasattr(tweet, "full_text"):
                tweets.append(tweet.full_text)
    except Exception as e:
        print(f"Error: {e}")
    return tweets

# Build AI pipeline for classification
def build_ai_pipeline():
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words='english')),
        ('classifier', MultinomialNB())
    ])
    return pipeline

# Train the AI pipeline
def train_pipeline(pipeline, training_data, labels):
    pipeline.fit(training_data, labels)
    joblib.dump(pipeline, "ai_pipeline.pkl")
    print("Pipeline trained and saved.")

# Load trained AI pipeline
def load_pipeline():
    try:
        pipeline = joblib.load("ai_pipeline.pkl")
        return pipeline
    except FileNotFoundError:
        print("Trained pipeline not found. Train the model first.")
        return None

# Evaluate collected tweets
def evaluate_tweets(pipeline, tweets):
    cleaned_tweets = [clean_tweet(tweet) for tweet in tweets]
    predictions = pipeline.predict(cleaned_tweets)
    positive_tweets = [tweets[i] for i, label in enumerate(predictions) if label == 1]
    return positive_tweets

if __name__ == "__main__":
    api = authenticate_twitter()
    hashtag = "#CryptoInvestment"
    
    # Collect tweets
    print("Collecting tweets...")
    tweets = collect_tweets(api, hashtag)
    print(f"Collected {len(tweets)} tweets.")

    # Train AI pipeline (This step requires labeled training data)
    # Example training data
    training_data = ["Bitcoin is the future", "Crypto is a scam", "Invest in Ethereum"]
    labels = [1, 0, 1]  # 1 for positive, 0 for negative
    
    pipeline = build_ai_pipeline()
    train_pipeline(pipeline, training_data, labels)

    # Load pipeline and evaluate tweets
    pipeline = load_pipeline()
    if pipeline:
        positive_tweets = evaluate_tweets(pipeline, tweets)
        print("Positive tweets:")
        for tweet in positive_tweets:
            print(tweet)
