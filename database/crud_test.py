from typing import List

from sqlalchemy.orm import Session

from . import models, schemas




def create_tweet(db: Session, tweet: schemas.TweetCreate) -> models.Tweet:
    """Uses the ORM to add a tweet into the database"""
    db_tweet = models.Tweet(
        text=tweet.text, favorites=tweet.favorites, is_retweet=tweet.is_retweet
    )
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def read_tweet(db: Session, tweet_id: int) -> models.Tweet:
    """Uses the ORM to query the database for a tweet by its id"""
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()


def read_tweets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tweet]:
    """Uses the ORM to query the database for the first n=limit tweets"""
    return db.query(models.Tweet).offset(skip).limit(limit).all()

def update_tweet(db: Session, tweet_id: int, labeled: int, is_funny: int) -> models.Tweet:
    """Update the tweet label_funny value"""
    results = db.query(tweet_id, labeled, is_funny)
    return results

def delete_tweet(db: Session, tweet_id: int) -> models.Tweet:
    """Uses the ORM to delete a tweet by its id"""
    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).delete()
    db.commit()
#Added functions get_users and get_unlabeled_tweets
def get_users(db: Session) -> List[models.Tweet.usernames]:

    return db.query(models.Tweet.usernames)

def get_unlabeled_tweets(db: Session) -> List[models.Tweet.labeled]:

    return db.query((models.Tweet.labeled).filter(models.Tweet.labeled == False)).all()
