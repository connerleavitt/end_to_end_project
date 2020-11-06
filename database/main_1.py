# from typing import List
#Step 1: Import FastAPI

#from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.testclient import TestClient
#from sqlalchemy.orm import Session

#from .database import crud, schemas #models
#from .database import SessionLocal, engine

#models.Base.metadata.create_all(bind=engine)

#Step 2: Create a FastAPI Instance
app = FastAPI(debug=True)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#Step 3: Create a path operation - (Path refers to the last part of the URL starting with /
# ... A "path" is also commonly called an "endpoint" or a "route".)
# Define Path operator (POST: create, GET: read, PUT: update, DELETE: delete)

#Define a path operator decorator
#Step 4: Path operation function
@app.get("/")
async def root():
    return {"message": "Hello World"}


#The @something syntax is called a decorator
#The value in the url path will be passed as a parameter
# @app.post("/tweets/", response_model=schemas.Tweet)
# def create_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
#     db_tweet = crud.read_tweet(db, tweet_id=tweet.id)
#     if db_tweet:
#         raise HTTPException(status_code=400, detail="Already in database")
#     return crud.create_tweet(db=db, tweet=tweet)


#
# @app.get("/tweets/", response_model=List[schemas.Tweet])
# def read_tweets(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
#     tweets = crud.read_tweets(db, skip=skip, limit=limit)
#     return tweets
#
#
# @app.get("/tweets/{tweet_id}", response_model=schemas.Tweet)
# def read_tweet(tweet_id: int, db: Session = Depends(get_db)):
#     db_tweet = crud.read_tweet(db, tweet_id=tweet_id)
#     if db_tweet is None:
#         raise HTTPException(status_code=404, detail="Tweet not found")
#     return db_tweet




