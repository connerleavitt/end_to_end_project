from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Tweet(Base):
    __tablename__ = "tweets"
    # TODO Figure out all the columns we want to use
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    favorites = Column(Integer)
    is_retweet = Column(Boolean, default=True)
