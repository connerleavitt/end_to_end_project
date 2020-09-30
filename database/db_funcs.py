from typing import List

from . import models
from .crud import create_tweet, delete_tweet, read_tweet, read_tweets
from .main import get_db
from .schemas import TweetCreate


def post_tweets(tweets: List):
    for tweet in tweets:
        tweet_to_add = TweetCreate(
            text=tweet["text"],
            favorites=tweet["favorites"],
            is_retweet=tweet["is_retweet"],
        )
        try:
            db = next(get_db())
            create_tweet(db, tweet_to_add)
        finally:
            db.close()


def get_tweets(count: int = 100) -> List[models.Tweet]:
    try:
        db = next(get_db())
        tweets = read_tweets(db, limit=count)
    finally:
        db.close()
    return tweets


def get_tweet(tweet_id: int) -> models.Tweet:
    try:
        db = next(get_db())
        tweet = read_tweet(db, tweet_id)
    finally:
        db.close()
    return tweet


def remove_tweets(ids: List[int]):
    for tweet_id in ids:
        try:
            db = next(get_db())
            delete_tweet(db, tweet_id)
        finally:
            db.close()
