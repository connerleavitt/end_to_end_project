from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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


@app.post("/tweets/", response_model=schemas.Tweet)
def create_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    db_tweet = crud.get_tweet(db, tweet_id=tweet.id)
    if db_tweet:
        raise HTTPException(status_code=400, detail="Already in database")
    return crud.create_tweet(db=db, tweet=tweet)


@app.get("/tweets/", response_model=List[schemas.Tweet])
def read_tweets(limit: int, skip: int = 0, db: Session = Depends(get_db)):
    tweets = crud.get_tweets(db, skip=skip, limit=limit)
    return tweets


@app.get("/tweets/{tweet_id}", response_model=schemas.Tweet)
def read_tweet(tweet_id: int, db: Session = Depends(get_db)):
    db_tweet = crud.get_tweet(db, tweet_id=tweet_id)
    if db_tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return db_tweet
