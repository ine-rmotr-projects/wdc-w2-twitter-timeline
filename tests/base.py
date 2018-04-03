import pytest
from django_webtest import WebTest

from twitter.models import Tweet, User


@pytest.fixture
def base_twitter_fixture(django_app, django_user_model):
    # Wiping out initial data created by migrations
    Tweet.objects.all().delete()
    User.objects.all().delete()

    jack = User.objects.create_user(
        username='jack', email='jack@twitter.com', password='coffee')
    ev = User.objects.create_user(
        username='evan', email='ev@twitter.com', password='coffee')
    larry = User.objects.create_user(
        username='larry', email='larry@twitter.com', password='coffee')

    return {
        'jack': jack,
        'ev': ev,
        'larry': larry
    }


@pytest.fixture
def base_authenticated_fixture(base_twitter_fixture, django_app):
    jack = base_twitter_fixture['jack']
    form = django_app.get('/login').form
    form['username'] = jack.username
    form['password'] = 'coffee'
    resp = form.submit().follow()

    assert resp.status_code, "Couldn't authenticate user"

    return base_twitter_fixture
