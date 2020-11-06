from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Tweet(Base):
    """A class defining the tweet object that will be used by the ORM"""

    __tablename__ = "tweets"
    # TODO Figure out all the columns we want to use
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    favorites = Column(Integer)
    is_retweet = Column(Boolean, default=True)
    #Updated fields usernames and labeled
    usernames = Column(String)
    labeled = Column(int)
    is_funny = Column(int)


    def __repr__(self):
        """Instances of the class will show the parts of the tweet"""
        return "Tweet(id: {}, text: {}, favorites: {}, is_retweet: {})".format(
            self.id, self.text, self.favorites, self.is_retweet, self.usernames, self.labeled, self.is_funny #usernames and labeled added
        )
