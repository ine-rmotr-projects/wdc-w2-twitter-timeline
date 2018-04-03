from datetime import datetime

from django.contrib.auth import get_user_model
from django_webtest import WebTest

from twitter.models import Tweet

User = get_user_model()


class TweetTimelineTestCase(WebTest):
    def setUp(self):
        # Wiping out initial data created by migrations
        Tweet.objects.all().delete()
        User.objects.all().delete()

        self.jack = User.objects.create_user(
            username='jack', email='jack@twitter.com', password='coffee')
        self.ev = User.objects.create_user(
            username='evan', email='ev@twitter.com', password='coffee')
        self.larry = User.objects.create_user(
            username='larry', email='larry@twitter.com', password='coffee')

    def test_timeline(self):
        """Should list tweets from both authenticated user and users that he is following"""
        # Preconditions
        self.jack.follow(self.ev)
        self.jack.follow(self.larry)
        Tweet.objects.create(user=self.jack, content='Tweet Jack 1')
        Tweet.objects.create(user=self.ev, content='Tweet Evan 1')
        Tweet.objects.create(user=self.larry, content='Tweet Larry 1')
        self.assertEqual(Tweet.objects.count(), 3)

        # first user timeline
        resp = self.app.get('/', user=self.jack)
        feed = resp.html.find('div', class_='tweet-feed')
        tweets = feed.find_all('div', class_='tweet-container')
        tweet_contents = [tweet.find('div', class_='tweet-content').text
                          for tweet in tweets]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(tweets), 3)
        self.assertTrue('Tweet Jack 1' in tweet_contents)
        self.assertTrue('Tweet Evan 1' in tweet_contents)
        self.assertTrue('Tweet Larry 1' in tweet_contents)

        # second user timeline
        resp = self.app.get('/', user=self.ev)
        feed = resp.html.find('div', class_='tweet-feed')
        tweets = feed.find_all('div', class_='tweet-container')
        tweet_contents = [tweet.find('div', class_='tweet-content').text
                          for tweet in tweets]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(tweets), 1)
        self.assertTrue('Tweet Evan 1' in tweet_contents)

        self.assertFalse('Tweet Jack 1' in tweet_contents)
        self.assertFalse('Tweet Larry 1' in tweet_contents)

    def test_timeline_tweets_ordering(self):
        """Should list tweets in timeline ordered by creation datetime"""
        self.jack.follow(self.ev)
        tw1 = Tweet.objects.create(user=self.jack, content='Tweet Jack 1')
        tw1.created = datetime(2015, 6, 22, 21, 55, 10)
        tw1.save()

        tw2 = Tweet.objects.create(user=self.ev, content='Tweet Evan 1')
        tw2.created = datetime(2014, 6, 22, 21, 55, 10)
        tw2.save()

        tw3 = Tweet.objects.create(user=self.jack, content='Tweet Jack 2')
        tw3.created = datetime(2016, 6, 22, 21, 55, 10)
        tw3.save()

        resp = self.app.get('/', user=self.jack)
        feed = resp.html.find('div', class_='tweet-feed')
        tweets = feed.find_all('div', class_='tweet-container')
        self.assertTrue('06/22/2016 9:55 p.m.' in
                        tweets[0].find('span', class_='created-datetime').text)
        self.assertTrue('06/22/2015 9:55 p.m.' in
                        tweets[1].find('span', class_='created-datetime').text)
        self.assertTrue('06/22/2014 9:55 p.m.' in
                        tweets[2].find('span', class_='created-datetime').text)

    def test_timeline_follow_button(self):
        """Should show follow button when authenticated user is not following current twitter profile"""
        # Preconditions
        resp = self.app.get('/evan', user=self.jack)
        button = resp.html.find('div', class_='relationship-button')
        self.assertTrue('Follow' in button.text)

        self.jack.follow(self.ev)

        # Postconditions
        resp = self.app.get('/evan', user=self.jack)
        button = resp.html.find('div', class_='relationship-button')
        self.assertFalse('Follow' in button.text)

    def test_timeline_follow_user(self):
        """Should create a Relationship between authenticated user and given twitter profile"""
        # Preconditions
        self.assertEqual(self.jack.count_following, 0)
        self.assertEqual(self.ev.count_followers, 0)
        self.assertFalse(self.jack.is_following(self.ev))

        resp = self.app.get('/evan', user=self.jack)
        form = resp.forms['follow-{}'.format(self.ev.username)]
        follow_user = form.submit()

        # Postconditions
        self.assertEqual(follow_user.status_code, 302)
        self.assertEqual(self.jack.count_following, 1)
        self.assertEqual(self.ev.count_followers, 1)
        self.assertTrue(self.jack.is_following(self.ev))

    def test_timeline_unfollow_button(self):
        """Should show unfollow button when authenticated user is following current twitter profile"""
        # Preconditions
        self.jack.follow(self.ev)
        resp = self.app.get('/evan', user=self.jack)
        button = resp.html.find('div', class_='relationship-button')
        self.assertTrue('Unfollow' in button.text)

        self.jack.unfollow(self.ev)

        # Postconditions
        resp = self.app.get('/evan', user=self.jack)
        button = resp.html.find('div', class_='relationship-button')
        self.assertFalse('Unfollow' in button.text)

    def test_timeline_unfollow_user(self):
        """Should delete a Relationship between authenticated user and given twitter profile"""
        # Preconditions
        self.jack.follow(self.ev)
        self.assertEqual(self.jack.count_following, 1)
        self.assertEqual(self.ev.count_followers, 1)
        self.assertTrue(self.jack.is_following(self.ev))

        resp = self.app.get('/evan', user=self.jack)
        form = resp.forms['unfollow-{}'.format(self.ev.username)]
        follow_user = form.submit()

        # Postconditions
        self.assertEqual(follow_user.status_code, 302)
        self.assertEqual(self.jack.count_following, 0)
        self.assertEqual(self.ev.count_followers, 0)
        self.assertFalse(self.jack.is_following(self.ev))
