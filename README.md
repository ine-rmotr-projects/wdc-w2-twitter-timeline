# Twitter Timeline

For this project we'll have to extend our previous Twitter clone to include the "following" and "timeline" features. You'll also need to write a data migration to change the way we used to store our tweets. For that, check the `tests/test_models.py` test case.

## Follow/Unfollow

When we're browsing some user's feed, we'll need to see a _follow/unfollow_ button (check screenshots below).

### Browsing a user I'm not following

![image](https://cloud.githubusercontent.com/assets/872296/18026719/d71d633c-6c26-11e6-814d-3b29fff9fe0f.png)

### Browsing a user I'm following

![image](https://cloud.githubusercontent.com/assets/872296/18026721/e7f9dfb4-6c26-11e6-8296-05670d7a739c.png)

## Timeline

For this project, when we browse our home page (`/`), we'll need to see a timeline of tweets constructed by our tweets and all the tweets from those users we're following, sorted historically.

![twitter clone](https://cloud.githubusercontent.com/assets/872296/18026739/64dea50a-6c27-11e6-89ec-d05e39ebd545.png)
