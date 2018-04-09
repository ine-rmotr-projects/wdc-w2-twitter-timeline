from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from model_utils.models import TimeStampedModel


class Tweet(TimeStampedModel):
    class Meta:
        ordering = ['-created']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)
    content = models.CharField(max_length=140, blank=True)


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


class Like(TimeStampedModel):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=Like)
def add_like_to_tweet(sender, instance, created, **kwargs):
    tweet = instance.tweet
    tweet.likes_count += 1
    tweet.save()

@receiver(post_delete, sender=Like)
def remove_like_from_tweet(sender, instance, **kwargs):
    tweet = instance.tweet
    tweet.likes_count -= 1
    tweet.save()
