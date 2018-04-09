from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

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
    tweets = Tweet.objects.filter(user=user)
    return render(request, 'feed.html', {
        'form': form,
        'twitter_profile': user,
        'tweets': tweets
    })


@login_required()
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        raise PermissionDenied
    tweet.delete()
    messages.success(request, 'Tweet successfully deleted')
    return redirect(request.GET.get('next', '/'))


@login_required()
@require_POST
def follow(request):
    pass


@login_required()
@require_POST
def unfollow(request):
    pass


@login_required()
def like_tweet(request, tweet_id):
    pass
