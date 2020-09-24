from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Tweet(Base):
    __tablename__ = "tweets"
    # TODO Figure out all the columns we want to use
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    favorites = Column(Integer)
    is_retweet = Column(Boolean, default=True)

    def __repr__(self):
        return "Tweet(id: {}, text: {}, favorites: {}, is_retweet: {})".format(
            self.id,
            self.text,
            self.favorites,
            self.is_retweet
        )
