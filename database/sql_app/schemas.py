from typing import List, Optional

from pydantic import BaseModel


class TweetBase(BaseModel):
    text: str
    favorites: int
    is_retweet: bool


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True
