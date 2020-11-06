from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

############## Tweets ##############
@app.post("/tweets/", response_model=schemas.Tweet)
def create_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    db_tweet = crud.read_tweet(db, tweet_id=tweet.id)
    if db_tweet:
        raise HTTPException(status_code=400, detail="Already in database")
    return crud.create_tweet(db=db, tweet=tweet)

@app.get("/tweets/", response_model=List[schemas.Tweet])
def read_tweets(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    tweets = crud.read_tweets(db, skip=skip, limit=limit)
    return tweets


@app.get("/tweets/{tweet_id}", response_model=schemas.Tweet)
def read_tweet(tweet_id: int, db: Session = Depends(get_db)):
    db_tweet = crud.read_tweet(db, tweet_id=tweet_id)
    if db_tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return db_tweet

############## Usernames ##############
@app.get("/users/", response_model=List[schemas.Tweet.usernames])
def get_usernames(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

############## Unlabeled Tweets ##############
#Get list of unlabeled tweets to further label
@app.get("/unlabeled_tweets/", response_model=List[schemas.Tweet])
def get_unlabeled_tweets(db: Session = Depends(get_db)):
    unlabeled_tweets = crud.get_unlabeled_tweets(db)

    return unlabeled_tweets

@app.get("/unlabeled_tweets/{tweet_id}", response_model=schemas.Tweet)
def read_tweet(tweet_id: int, db: Session = Depends(get_db)):
    db_tweet = crud.read_tweet(db, tweet_id=tweet_id)
    if db_tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return db_tweet

@app.put("/unlabeled_tweets/{tweet_id}", response_model=schemas.Tweet)
async def update_tweet(tweet_id: int, labeled: int, is_funny: int, db: Session = Depends(get_db)):
    updated_is_funny = jsonable_encoder(is_funny)
    new_label = labeled

    ######### Items to update #########
    ## is_funny
    ## labeled

    ######### Items to persist #########
    ## tweet_id = Column(Integer, primary_key=True, index=True)
    ## text = Column(String, unique=True, index=True)
    ## favorites = Column(Integer)
    ## is_retweet = Column(Boolean, default=True)
    ## usernames = Column(String)

    db_tweet = crud.update_tweet(db, tweet_id, updated_is_funny, new_label)

    return db_tweet

# How do I Update newly labeled tweets?
# What is the way we can update the database after the tweet is clicked?
#
