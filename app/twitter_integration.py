```python
import tweepy

class TwitterAPI:
    def __init__(self, handle):
        self.api = tweepy.Client(bearer_token="<BEARER_TOKEN>")
        self.handle = handle

    def get_mentions(self):
        """Fetch recent mentions from Twitter."""
        mentions = self.api.get_users_mentions(id=self.handle)
        return mentions.data if mentions else []

    def post_update(self, message):
        """Post an update to Twitter."""
        self.api.create_tweet(text=message)
```

---
