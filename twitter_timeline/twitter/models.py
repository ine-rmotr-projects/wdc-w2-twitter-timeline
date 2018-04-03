from django.db import models


class Tweet(models.Model):
    # {
    #     "username": "jack",
    #     "content": "hello world!",
    #     "created": "2016-08-26T10:03:28"
    # }
    tweet_info_json = models.CharField(max_length=1500)
