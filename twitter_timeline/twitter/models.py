from django.db import models
from django.contrib.auth.models import AbstractUser


class Tweet(models.Model):
    pass


class Relationship(models.Model):
    pass


class User(AbstractUser):

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass

    def is_following(self, user):
        pass

    @property
    def following(self):
        pass

    @property
    def followers(self):
        pass

    @property
    def count_following(self):
        pass

    @property
    def count_followers(self):
        pass

class Like(models.Model):
    pass
