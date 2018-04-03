from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import utc

from twitter.models import Tweet

User = get_user_model()


class TwitterDataTestCase(TestCase):
    def test_tweets_are_migrated(self):
        self.assertEqual(Tweet.objects.count(), 2)
        jack = User.objects.get(username='jack')
        ev = User.objects.get(username='ev')
        jacks_tweet = Tweet.objects.get(content='just setting up my twttr')
        evs_tweet = Tweet.objects.get(content='checking out twttr')

        self.assertEqual(
            jacks_tweet.created, datetime(2006, 3, 21, 2, 50, tzinfo=utc))
        self.assertEqual(
            evs_tweet.created, datetime(2006, 3, 21, 5, 51, tzinfo=utc))

        self.assertEqual(jacks_tweet.user, jack)
        self.assertEqual(evs_tweet.user, ev)
