from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel



class Tweet(TimeStampedModel):
    class Meta:
        ordering = ['-created']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like')
    content = models.CharField(max_length=140, blank=True)

    @property
    def count_likes(self):
        return self.likes.count()

    @property
    def add_like_from_user(self, user):
        self.likes.add(user)

    @property
    def remove_like_from_user(self, user):
        self.likes.remove(user)


class Relationship(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='from_user',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='to_user',
        on_delete=models.CASCADE
    )


class User(AbstractUser):

    relationships = models.ManyToManyField(
        "self", through='Relationship', symmetrical=False,
        related_name='related_to'
    )

    def follow(self, twitter_profile):
        try:
            Relationship.objects.get(follower=self, following=twitter_profile)
        except Relationship.DoesNotExist:
            Relationship.objects.create(
                follower=self, following=twitter_profile)

    def unfollow(self, twitter_profile):
        try:
            rel = Relationship.objects.get(
                follower=self, following=twitter_profile)
        except Relationship.DoesNotExist:
            return
        rel.delete()

    def is_following(self, twitter_profile):
        return Relationship.objects.filter(
            follower=self, following=twitter_profile).exists()

    @property
    def following(self):
        return [rel.following for rel in
                Relationship.objects.filter(follower=self)]

    @property
    def followers(self):
        return [rel.following for rel in
                Relationship.objects.filter(following=self)]

    @property
    def count_following(self):
        return Relationship.objects.filter(follower=self).count()

    @property
    def count_followers(self):
        return Relationship.objects.filter(following=self).count()
