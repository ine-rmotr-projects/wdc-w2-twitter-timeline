import pytest
from datetime import datetime

from django.utils.timezone import utc

from twitter.models import Tweet, User
from base import base_twitter_fixture, base_authenticated_fixture


def test_tweets_are_migrated():
    assert Tweet.objects.count() == 2
    jack = User.objects.get(username='jack')
    ev = User.objects.get(username='ev')
    jacks_tweet = Tweet.objects.get(content='just setting up my twttr')
    evs_tweet = Tweet.objects.get(content='checking out twttr')

    assert jacks_tweet.created, datetime(2006, 3, 21, 2, 50, tzinfo=utc)
    assert evs_tweet.created, datetime(2006, 3, 21, 5, 51, tzinfo=utc)

    assert jacks_tweet.user == jack
    assert evs_tweet.user == ev


def test_tweet_info(base_twitter_fixture):
    Tweet.objects.create(user=base_twitter_fixture['jack'], content='Tweet Jack 1')
    Tweet.objects.create(user=base_twitter_fixture['ev'], content='Tweet Evan 1')

    assert Tweet.objects.count() == 2
