import time
import webbrowser

import pandas as pd
import tweepy
import twitter_secrets as ts


class TwitterClient:
    def __init__(self):
        """Instantiates the tweepy API object and authenticates it"""

        self.auth = tweepy.OAuthHandler(ts.consumer_key, ts.consumer_secret)
        self.auth.set_access_token(ts.access_token, ts.access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_user_tweets(self, num_tweets: int, user: str) -> list:
        """Returns a list of n=count tweets from the user's timeline

        Parameters:
            num_tweets (int): The number of tweets to return
            user (str): The username of the user's tweets being pulled
        Returns:
            (list): A list containing the n=count tweets retrieved from the user's timeline
        """

        tweets = []
        for tweet in tweepy.Cursor(
            self.api.user_timeline, id=user, count=100, tweet_mode="extended"
        ).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_search_tweets(self, num_tweets: int, query: str) -> list:
        """Returns a list of n=count tweets matching the search query

        Parameters:
            num_tweets (int): The number of tweets to return
            query (str): The twitter search query to use for matching tweets
        Returns:
            (list): A list containing the n=count tweets retrieved matching the search query
        """
        tweets = []
        for tweet in tweepy.Cursor(
            self.api.search,
            q=query,
            count=100,
            result_type="recent",
            lang="en",
            tweet_mode="extended",
        ).items(num_tweets):
            tweets.append(tweet)
        return tweets
