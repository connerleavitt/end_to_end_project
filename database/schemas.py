from pydantic import BaseModel


class TweetBase(BaseModel):
    """A class for the database table schema"""

    text: str
    user: str
    search_query: str
    favorite_count: int
    retweet_count: int
    follower_count: int
    media: bool
    is_reply: bool
    is_retweet: bool
    has_mentions: bool
    is_funny: bool
    label_funny: bool = None


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    """A separate class containing the id which is assigned by the ORM not the user"""

    id: int

    class Config:
        orm_mode = True
