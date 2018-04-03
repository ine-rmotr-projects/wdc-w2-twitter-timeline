# from datetime import datetime
# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
# from twitter.models import Tweet
#
# User = get_user_model()
#
#
# class TwitterDataTestCase(TestCase):
#     def test_tweet_info(self):
#         self.assertEqual(Tweet.objects.count(), 2)
#         evs_tweet = Tweet.objects.get(content='checking out twttr')
#         # Test created, content and user are not null


import pytest

from twitter.models import Tweet
from base import base_twitter_fixture, base_authenticated_fixture


def test_tweet_info(base_twitter_fixture):
    Tweet.objects.create(user=base_twitter_fixture['jack'], content='Tweet Jack 1')
    Tweet.objects.create(user=base_twitter_fixture['ev'], content='Tweet Evan 1')

    assert Tweet.objects.count() == 2
