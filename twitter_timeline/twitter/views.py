from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.http.response import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as django_logout, get_user_model

from .forms import TweetForm
from .models import Tweet, Relationship, User, Like


@login_required()
def logout(request):
    django_logout(request)
    return redirect('/')


def home(request, username=None):
    if not request.user.is_authenticated:
        if not username or request.method != 'GET':
            return redirect(settings.LOGIN_URL + '?next=%s' % request.path)

    user = request.user

    if request.method == 'POST':
        if username and username != user.username:
            return HttpResponseForbidden()
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            # Reset the form
            form = TweetForm()
            messages.success(request, 'Tweet Created!')
    else:
        form = TweetForm()
        if username is not None:
            user = get_object_or_404(get_user_model(), username=username)
            form = None
    users_following = request.user.following
    tweets = Tweet.objects.filter(Q(user=user) | Q(user__in=users_following))
    liked_tweets = [like.tweet for like in Like.objects.filter(user=user)]

    for tweet in tweets:
        if tweet in liked_tweets:
            tweet.is_liked_by_user = True
        else:
            tweet.is_liked_by_user = False

    following_profile = request.user.is_following(user)
    return render(request, 'feed.html', {
        'form': form,
        'twitter_profile': user,
        'tweets': tweets,
        'following_profile': following_profile
    })


@login_required()
@require_POST
def follow(request):
    followed = get_object_or_404(
        get_user_model(), username=request.POST['username'])
    request.user.follow(followed)
    return redirect(request.GET.get('next', '/'))


@login_required()
@require_POST
def unfollow(request):
    unfollowed = get_object_or_404(
        get_user_model(), username=request.POST['username'])
    request.user.unfollow(unfollowed)
    return redirect(request.GET.get('next', '/'))


@login_required()
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        raise PermissionDenied
    tweet.delete()
    messages.success(request, 'Tweet successfully deleted')
    return redirect(request.GET.get('next', '/'))


@login_required()
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    try:
        like = Like.objects.get(user=request.user, tweet=tweet)
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, tweet=tweet)
    else:
        like.delete()
    return HttpResponse('')
