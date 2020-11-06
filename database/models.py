from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Tweet(Base):
    """A class defining the tweet object that will be used by the ORM"""

    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
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
=======
    text = Column(String(400), unique=True)
    user = Column(String(100))
    search_query = Column(String(100))
    favorite_count = Column(Integer)
    retweet_count = Column(Integer)
    follower_count = Column(Integer)
    media = Column(Boolean)
    is_reply = Column(Boolean)
    is_retweet = Column(Boolean)
    has_mentions = Column(Boolean)
    is_funny = Column(Boolean, nullable=True)
    label_funny = Column(Boolean, nullable=True)

    def __repr__(self):
        """Instances of the class will show the parts of the tweet"""
        return "Tweet(id: {}, text: {}, user: {}, label: {})".format(
            self.id, self.text[:200].replace("\n", ""), self.user, self.is_funny
>>>>>>> 75e9f6581f27b21f05b2d2b07bc670082d8fe3b7
        )
