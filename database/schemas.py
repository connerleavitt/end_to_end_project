from pydantic import BaseModel


class TweetBase(BaseModel):
    """A class for the database table schema"""

    text: str
    favorites: int
    is_retweet: bool


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    """A separate class containing the id which is assigned by the ORM not the user"""

    id: int

    class Config:
        orm_mode = True
