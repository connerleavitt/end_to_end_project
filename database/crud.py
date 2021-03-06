from typing import List

import numpy as np
from sqlalchemy.orm import Session, query

from . import models, schemas


def unlabeled_tweet(db: Session) -> models.Tweet:
    """Returns a randomly selected unlabeled tweet for manual labeling"""
    unlabeled_tweets = (
        db.query(models.Tweet).filter(models.Tweet.label_funny is None).all()
    )
    return unlabeled_tweets[np.random.randint(len(unlabeled_tweets))]


def label_tweet(db: Session, tweet_id: int, man_label: bool):
    """Updates the manual label for a tweet"""
    tweet_to_update = db.query(models.Tweet).get(tweet_id)
    tweet_to_update.label_funny = man_label
    try:
        db.commit()
    except Exception as e:
        print(e)


def custom_query(db: Session) -> query.Query:
    """Returns a sqlalchemy.orm.query.Query object so that custom queries can be written"""
    return db.query(models.Tweet)


def read_tweet(db: Session, tweet_id: int) -> models.Tweet:
    """Uses the ORM to query the database for a tweet by its id"""
    return db.query(models.Tweet).get(tweet_id).first()


def read_tweets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tweet]:
    """Uses the ORM to query the database for the first n=limit tweets"""
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_tweet(db: Session, tweet: schemas.TweetCreate) -> models.Tweet:
    """Uses the ORM to add a tweet into the database"""
    db_tweet = models.Tweet(
        text=tweet.text,
        user=tweet.user,
        search_query=tweet.search_query,
        favorite_count=tweet.favorite_count,
        retweet_count=tweet.retweet_count,
        follower_count=tweet.follower_count,
        media=tweet.media,
        is_reply=tweet.is_reply,
        is_retweet=tweet.is_retweet,
        has_mentions=tweet.has_mentions,
        is_funny=tweet.is_funny,
        label_funny=tweet.label_funny,
    )
    try:
        db.add(db_tweet)
        db.commit()
        db.refresh(db_tweet)
    except Exception as e:
        print(e)
    return db_tweet


def create_tweets(db: Session, tweets: List[schemas.TweetCreate]) -> models.Tweet:
    """Uses the ORM to add a batch of tweets into the database all at once"""
    tweets = [
        models.Tweet(
            text=tweet.text,
            user=tweet.user,
            search_query=tweet.search_query,
            favorite_count=tweet.favorite_count,
            retweet_count=tweet.retweet_count,
            follower_count=tweet.follower_count,
            media=tweet.media,
            is_reply=tweet.is_reply,
            is_retweet=tweet.is_retweet,
            has_mentions=tweet.has_mentions,
            is_funny=tweet.is_funny,
            label_funny=tweet.label_funny,
        )
        for tweet in tweets
    ]
    try:
        db.add_all(tweets)
        db.commit()
    except Exception as e:
        print(e)
    return len(tweets)


def delete_tweet(db: Session, tweet_id: int) -> models.Tweet:
    """Uses the ORM to delete a tweet by its id"""
    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).delete()
    db.commit()


def delete_all_tweets(db: Session) -> models.Tweet:
    """Uses the ORM to delete all tweets"""
    db.query(models.Tweet).delete()
    db.commit()


def delete_user_tweets(db: Session, username: str) -> models.Tweet:
    """Uses the ORM to delete a tweet by its id"""
    db.query(models.Tweet).filter(models.Tweet.user == username).delete()
    db.commit()
