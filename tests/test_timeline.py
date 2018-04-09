import pytest
from datetime import datetime

from twitter.models import Tweet, Like
from base import base_twitter_fixture, base_authenticated_fixture


def test_timeline(base_twitter_fixture, django_app):
    """Should list tweets from both authenticated user and users that he is following"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']
    larry = base_twitter_fixture['larry']

    # Preconditions
    jack.follow(ev)
    jack.follow(larry)
    Tweet.objects.create(user=jack, content='Tweet Jack 1')
    Tweet.objects.create(user=ev, content='Tweet Evan 1')
    Tweet.objects.create(user=larry, content='Tweet Larry 1')
    assert Tweet.objects.count() == 3

    # first user timeline
    resp = django_app.get('/', user=jack)
    feed = resp.html.find('div', class_='tweet-feed')
    tweets = feed.find_all('div', class_='tweet-container')
    tweet_contents = [tweet.find('div', class_='tweet-content').text
                      for tweet in tweets]
    assert resp.status_code == 200
    assert len(tweets) == 3
    assert 'Tweet Jack 1' in tweet_contents
    assert 'Tweet Evan 1' in tweet_contents
    assert 'Tweet Larry 1' in tweet_contents

    # second user timeline
    resp = django_app.get('/', user=ev)
    feed = resp.html.find('div', class_='tweet-feed')
    tweets = feed.find_all('div', class_='tweet-container')
    tweet_contents = [tweet.find('div', class_='tweet-content').text
                      for tweet in tweets]
    assert resp.status_code == 200
    assert len(tweets) == 1
    assert 'Tweet Evan 1' in tweet_contents

    assert 'Tweet Jack 1' not in tweet_contents
    assert 'Tweet Larry 1' not in tweet_contents

def test_timeline_tweets_ordering(base_twitter_fixture, django_app):
    """Should list tweets in timeline ordered by creation datetime"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    jack.follow(ev)
    tw1 = Tweet.objects.create(user=jack, content='Tweet Jack 1')
    tw1.created = datetime(2015, 6, 22, 21, 55, 10)
    tw1.save()

    tw2 = Tweet.objects.create(user=ev, content='Tweet Evan 1')
    tw2.created = datetime(2014, 6, 22, 21, 55, 10)
    tw2.save()

    tw3 = Tweet.objects.create(user=jack, content='Tweet Jack 2')
    tw3.created = datetime(2016, 6, 22, 21, 55, 10)
    tw3.save()

    resp = django_app.get('/', user=jack)
    feed = resp.html.find('div', class_='tweet-feed')
    tweets = feed.find_all('div', class_='tweet-container')
    assert '06/22/2016 9:55 p.m.' in tweets[0].find('span', class_='created-datetime').text
    assert '06/22/2015 9:55 p.m.' in tweets[1].find('span', class_='created-datetime').text
    assert '06/22/2014 9:55 p.m.' in tweets[2].find('span', class_='created-datetime').text

def test_timeline_follow_button(base_twitter_fixture, django_app):
    """Should show follow button when authenticated user is not following current twitter profile"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    # Preconditions
    resp = django_app.get('/evan', user=jack)
    button = resp.html.find('div', class_='relationship-button')
    assert 'Follow' in button.text

    jack.follow(ev)

    # Postconditions
    resp = django_app.get('/evan', user=jack)
    button = resp.html.find('div', class_='relationship-button')
    assert 'Follow' not in button.text

def test_timeline_follow_user(base_twitter_fixture, django_app):
    """Should create a Relationship between authenticated user and given twitter profile"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    # Preconditions
    assert jack.count_following == 0
    assert ev.count_followers == 0
    assert jack.is_following(ev) == False

    resp = django_app.get('/evan', user=jack)
    form = resp.forms['follow-{}'.format(ev.username)]
    follow_user = form.submit()

    # Postconditions
    assert follow_user.status_code == 302
    assert jack.count_following == 1
    assert ev.count_followers == 1
    assert jack.is_following(ev)

def test_timeline_unfollow_button(base_twitter_fixture, django_app):
    """Should show unfollow button when authenticated user is following current twitter profile"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    # Preconditions
    jack.follow(ev)
    resp = django_app.get('/evan', user=jack)
    button = resp.html.find('div', class_='relationship-button')
    assert 'Unfollow' in button.text

    jack.unfollow(ev)

    # Postconditions
    resp = django_app.get('/evan', user=jack)
    button = resp.html.find('div', class_='relationship-button')
    assert 'Unfollow' not in button.text

def test_timeline_unfollow_user(base_twitter_fixture, django_app):
    """Should delete a Relationship between authenticated user and given twitter profile"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    # Preconditions
    jack.follow(ev)
    assert jack.count_following == 1
    assert ev.count_followers == 1
    assert jack.is_following(ev)

    resp = django_app.get('/evan', user=jack)
    form = resp.forms['unfollow-{}'.format(ev.username)]
    follow_user = form.submit()

    # Postconditions
    assert follow_user.status_code == 302
    assert jack.count_following == 0
    assert ev.count_followers == 0
    assert jack.is_following(ev) == False

def test_like_tweet_signals(base_twitter_fixture, django_app):
    """Should increment/decrease Tweet's likes_count when Like object is created/removed for that tweet"""
    jack = base_twitter_fixture['jack']
    ev = base_twitter_fixture['ev']

    # Preconditions
    tw = Tweet.objects.create(user=jack, content='Tweet Jack 1')
    assert Tweet.objects.count() == 1
    assert tw.likes_count == 0
    assert Like.objects.count() == 0

    like = Like.objects.create(user=ev, tweet=tw)

    # Postconditions
    assert Like.objects.count() == 1
    tw = Tweet.objects.get(user=jack)
    assert tw.likes_count == 1

    like.delete()
    tw = Tweet.objects.get(user=jack)
    assert tw.likes_count == 0
