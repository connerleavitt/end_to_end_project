from pydantic import BaseModel


class TweetBase(BaseModel):
    """A class for the database table schema"""

    #General Data
    text: str #check
    user: str #check
    media: bool #yes

    #Count fields
    favorite_count: int #yes
    retweet_count: int #yes
    follower_count: int #yes

    #Is fields
    is_reply: bool #yes
    is_retweet: bool #yes
    is_funny: bool #yes

    #hidden or input fields
    search_query: str #yes
    labeled: bool
    has_mentions: bool #yes
    #label_funny: bool = None

class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    """A separate class containing the id which is assigned by the ORM not the user"""

    id: int

    class Config:
        orm_mode = True
