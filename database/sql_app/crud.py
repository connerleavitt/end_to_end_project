from sqlalchemy.orm import Session

from . import models, schemas


def get_tweet(db: Session, tweet_id: int):
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()


def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_tweet(db: Session, tweet: schemas.TweetCreate):
    db_tweet = models.Tweet(text=tweet.text,
                            favorites=tweet.favorites,
                            is_retweet=tweet.is_retweet)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet
