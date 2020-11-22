from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Tweet(Base):
    """A class defining the tweet object that will be used by the ORM"""

    __tablename__ = "tweets"

    #General data
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    user = Column(String)
    media = Column(Boolean)

    # Count fields
    favorite_count = Column(Integer)
    retweet_count = Column(Integer)
    follower_count = Column(Integer)

    # Is fields
    is_retweet = Column(Boolean, default=True)
    is_funny = Column(Boolean, nullable=True)
    is_reply = Column(Boolean)
    is_retweet = Column(Boolean)
    is_funny = Column(Boolean, nullable=True)

    # hidden or input fields
    search_query = Column(String(100))
    labeled = Column(Boolean, nullable=True)
    has_mentions = Column(Boolean)


    def __repr__(self):
        """Instances of the class will show the parts of the tweet"""
        return "Tweet(id: {}, text: {}, favorites: {}, user: {}, is_retweet: {})".format(
            self.id, self.text[:200].replace("\n", ""), self.user, self.is_funny
        )
