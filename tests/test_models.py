from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from twitter.models import Tweet

User = get_user_model()


class TwitterDataTestCase(TestCase):
    def test_tweet_info(self):
        self.assertEqual(Tweet.objects.count(), 2)
        evs_tweet = Tweet.objects.get(content='checking out twttr')
        # Test created, content and user are not null
