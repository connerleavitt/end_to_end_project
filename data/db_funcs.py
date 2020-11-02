import html
import re
import time
from typing import List

import numpy as np
import pandas as pd
import rootpath
import tweepy
from sqlalchemy.orm import query
from tqdm import tqdm
from twitter_scraping import TwitterClient

# Allows us to import modules from our database package located in a separate directory
rootpath.append()

from database import models  # noqa: E402
from database.crud import (
    create_tweets,
    custom_query,  # noqa: E402
    delete_all_tweets,
    delete_tweet,
    delete_user_tweets,
    read_tweet,
    read_tweets,
)
from database.main import get_db  # noqa: E402
from database.schemas import TweetCreate  # noqa: E402


def media_cond(tweet: tweepy.models.Status) -> bool:
    """Contains the logic for finding whether or not there is media in a tweet"""
    if "retweeted_status" in tweet._json:
        return (
            tweet._json["retweeted_status"]["entities"]["urls"] != []
            or "media" in tweet._json["retweeted_status"]["entities"]
        )
    else:
        return tweet._json["entities"]["urls"] != [] or "media" in tweet._json["entities"]


def new_tweets_only(tweet_df: pd.DataFrame) -> int:
    """
    Puts tweets into the database. Gets rid of duplicates so that all new tweets can be added at
    the same time saving significant amounts of time.
    """
    tweets = [
        TweetCreate(
            text=tweet_df.iloc[i]["text"],
            user=tweet_df.iloc[i]["user"],
            search_query=tweet_df.iloc[i]["search_query"],
            favorite_count=tweet_df.iloc[i]["favorite_count"],
            retweet_count=tweet_df.iloc[i]["retweet_count"],
            follower_count=tweet_df.iloc[i]["follower_count"],
            media=tweet_df.iloc[i]["media"],
            is_reply=tweet_df.iloc[i]["is_reply"],
            is_retweet=tweet_df.iloc[i]["is_retweet"],
            has_mentions=tweet_df.iloc[i]["has_mentions"],
            is_funny=tweet_df.iloc[i]["is_funny"],
        )
        for i in range(len(tweet_df))
    ]
    try:
        # Gets a list containing the text of all tweets in the database
        db = next(get_db())
        tweet_text = [tweet.text for tweet in read_tweets(db, 0, 1000000)]
        db.close()
        # Creates a new list containing only the tweets not already in the database
        new_tweets = [tweet for tweet in tweets if tweet.text not in tweet_text]
        num_tweets = len(new_tweets)
        db = next(get_db())
        # Adds all of the new tweets as a batch
        print("Tweets filtered. Posting to database...")
        create_tweets(db, new_tweets)
    except Exception as e:
        print(e)
    finally:
        db.close()
    return num_tweets  # , tweet_text, new_tweets, tweet_df


def get_tweets(count: int = 100) -> List[models.Tweet]:
    """
    Gets the first n=count tweets from the database
    Parameters:
        count (int): the number of tweets to query from the database
    Returns:
        (list): A list containing the first n=count tweets from the database
    """
    try:
        db = next(get_db())
        tweets = read_tweets(db, limit=count)
    finally:
        db.close()
    return tweets


def get_tweet(tweet_id: int) -> models.Tweet:
    """
    Gets the tweet with the specified id from the database
    Parameters:
        tweet_id (int): the id of the tweet to query from the database
    Returns:
        (models.Tweet): A tweet object from the database with the specified id
    """
    try:
        db = next(get_db())
        tweet = read_tweet(db, tweet_id)
    finally:
        db.close()
    return tweet


def remove_tweets(ids: List[int]):
    """
    Deletes the specified tweets from the database
    Parameters:
        ids (list): A list containing the ids of the tweets to be deleted
    """
    for id in tqdm(ids):
        try:
            db = next(get_db())
            delete_tweet(db, id)
        finally:
            db.close()


def remove_all_tweets():
    """Empties the database"""
    try:
        db = next(get_db())
        delete_all_tweets(db)
    finally:
        db.close()


def search_tweets_to_db(search_query: str, label: bool, count: int = 18000):
    start = time.time()
    # Initializes and authorizes the twitter API client
    tc = TwitterClient()

    # Gets the n=count tweets using the search query
    print(f"Retrieving {count} tweets containing '{search_query}'...")
    tweets = tc.get_search_tweets(count, search_query)

    # Formats the tweets into a dataframe
    print("Tweets retrieved. Formatting...")
    # Ensures that the full text of the tweet is used
    df = pd.DataFrame(
        [
            tweet._json["full_text"]
            if "retweeted_status" not in tweet._json
            else tweet._json["retweeted_status"]["full_text"]
            for tweet in tweets
        ],
        columns=["text"],
    )
    # The user who tweeted/retweeted the tweet
    df["user"] = [tweet._json["user"]["screen_name"] for tweet in tweets]
    # Unescapes html entities ('&amp;' -> '&') and removes user handles ('@jack' -> '@')
    df["text"] = df["text"].apply(
        lambda x: html.unescape(re.sub(r"@\w+", "@", x))
        .lower()
        .replace("…", "...")
        .replace("\xa0", " ")
    )
    df["search_query"] = search_query
    # Numerical engagement data that may be used for analysis
    df["favorite_count"] = [tweet._json["favorite_count"] for tweet in tweets]
    df["retweet_count"] = [tweet._json["retweet_count"] for tweet in tweets]
    df["follower_count"] = [tweet._json["user"]["followers_count"] for tweet in tweets]
    # A binary column whether or not there is any media or urls in the tweet
    df["media"] = [media_cond(tweet) for tweet in tweets]
    # Whether or not the tweet is a reply
    df["is_reply"] = [
        False if tweet._json["in_reply_to_status_id"] is None else True
        for tweet in tweets
    ]
    # Whether or not the tweet was retweeted
    df["is_retweet"] = [
        True if "retweeted_status" in tweet._json else False for tweet in tweets
    ]
    # Whether or not the tweet contains user mentions
    df["has_mentions"] = df["text"].apply(lambda x: x.find("@") >= 0)
    # The automatic label given when the tweet was pulled
    df["is_funny"] = label
    # Initially empty column for hand labeled labels
    df["label_funny"] = np.nan
    # Drops any duplicates occurring from multiple retweets of the same tweet
    df.drop_duplicates(subset=["text"], inplace=True)

    # Adds all of the tweets in the dataframe to the database
    print("Tweets formatted. Filtering tweets...")
    num_tweets = new_tweets_only(df)
    print(f"{num_tweets} tweets added database in {time.time() - start} s")
    rl = tc.api.rate_limit_status()["resources"]["search"]["/search/tweets"]
    print(
        f'You can pull {rl["remaining"]*100} more search tweets in the next {int((rl["reset"] - time.time()) // 60)} min {int(((rl["reset"] - time.time()) % 60))} sec'
    )


def user_tweets_to_db(user_handle: str, label: bool, count: int = 18000):
    start = time.time()
    # Initializes and authorizes the twitter API client
    tc = TwitterClient()

    # Gets the n=count tweets from the specified user's timeline
    print(f"Retrieving {count} tweets from @{user_handle}...")
    tweets = tc.get_user_tweets(count, user_handle)

    # Formats the tweets into a dataframe
    print("Tweets retrieved. Formatting...")
    # Ensures that the full text of the tweet is used
    df = pd.DataFrame(
        [
            tweet._json["full_text"]
            if "retweeted_status" not in tweet._json
            else tweet._json["retweeted_status"]["full_text"]
            for tweet in tweets
        ],
        columns=["text"],
    )
    df = pd.DataFrame(
        [
            tweet._json["full_text"]
            if "retweeted_status" not in tweet._json
            else tweet._json["retweeted_status"]["full_text"]
            for tweet in tweets
        ],
        columns=["text"],
    )
    # The user who tweeted/retweeted the tweet
    df["user"] = [tweet._json["user"]["screen_name"] for tweet in tweets]
    # Unescapes html entities ('&amp;' -> '&') and removes user handles ('@jack' -> '@')
    df["text"] = df["text"].apply(
        lambda x: html.unescape(re.sub(r"@\w+", "@", x))
        .lower()
        .replace("…", "...")
        .replace("\xa0", " ")
    )
    # An '@' is prepended to the user handle to differentiate between search and user queries
    df["search_query"] = "@" + user_handle
    # Numerical engagement data that may be used for analysis
    df["favorite_count"] = [tweet._json["favorite_count"] for tweet in tweets]
    df["retweet_count"] = [tweet._json["retweet_count"] for tweet in tweets]
    df["follower_count"] = [tweet._json["user"]["followers_count"] for tweet in tweets]
    # A binary column whether or not there is any media or urls in the tweet
    df["media"] = [media_cond(tweet) for tweet in tweets]
    # Whether or not the tweet is a reply
    df["is_reply"] = [
        False if tweet._json["in_reply_to_status_id"] is None else True
        for tweet in tweets
    ]
    # Whether or not the tweet was retweeted
    df["is_retweet"] = [
        True if "retweeted_status" in tweet._json else False for tweet in tweets
    ]
    # Whether or not the tweet contains user mentions
    df["has_mentions"] = df["text"].apply(lambda x: x.find("@") >= 0)
    # The automatic label given when the tweet was pulled
    df["is_funny"] = label
    # Initially empty column for hand labeled labels
    df["label_funny"] = np.nan
    # Drops any duplicates occurring from multiple retweets of the same tweet
    df.drop_duplicates(subset=["text"], inplace=True)

    # Adds all of the tweets in the dataframe to the database
    print("Tweets formatted. Filtering tweets...")
    num_tweets = new_tweets_only(df)
    print(f"{num_tweets} tweets added database in {time.time() - start} s")
    rl = tc.api.rate_limit_status()["resources"]["statuses"]["/statuses/user_timeline"]
    print(
        f'You can pull {rl["remaining"]*100} more user tweets in the next {int((rl["reset"] - time.time()) // 60)} min {int(((rl["reset"] - time.time()) % 60))} sec'
    )
    # return num_tweets


def get_query() -> query.Query:
    """Returns a sqlalchemy.orm.query.Query object for custom queries"""
    db = next(get_db())
    return custom_query(db)


def query_to_df(tweets: List[models.Tweet]) -> pd.DataFrame:
    """Puts the results of a query into a pandas dataframe"""

    df = pd.DataFrame([tweet.id for tweet in tweets], columns=["id"])
    df["text"] = [tweet.text for tweet in tweets]
    df["user"] = [tweet.user for tweet in tweets]
    df["search_query"] = [tweet.search_query for tweet in tweets]
    df["favorite_count"] = [tweet.favorite_count for tweet in tweets]
    df["retweet_count"] = [tweet.retweet_count for tweet in tweets]
    df["follower_count"] = [tweet.follower_count for tweet in tweets]
    df["media"] = [tweet.media for tweet in tweets]
    df["is_reply"] = [tweet.is_reply for tweet in tweets]
    df["is_retweet"] = [tweet.is_retweet for tweet in tweets]
    df["has_mentions"] = [tweet.has_mentions for tweet in tweets]
    df["is_funny"] = [tweet.is_funny for tweet in tweets]
    df["label_funny"] = [tweet.label_funny for tweet in tweets]

    return df


def filter_db():
    """Deletes all items from the database that match certain filters"""
    usernames = ["Kada_soulayman", "SkowoH"]
    for username in usernames:
        try:
            db = next(get_db())
            delete_user_tweets(db, username)
        finally:
            db.close()
