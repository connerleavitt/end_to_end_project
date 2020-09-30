from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def read_tweet(db: Session, tweet_id: int) -> models.Tweet:
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()


def read_tweets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tweet]:
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_tweet(db: Session, tweet: schemas.TweetCreate) -> models.Tweet:
    db_tweet = models.Tweet(
        text=tweet.text, favorites=tweet.favorites, is_retweet=tweet.is_retweet
    )
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def delete_tweet(db: Session, tweet_id: int) -> models.Tweet:
    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).delete()
    db.commit()
