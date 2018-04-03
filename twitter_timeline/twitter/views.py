from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Tweet


@login_required()
def logout(request):
    django_logout(request)
    return redirect('/')


@login_required()
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user != request.user:
        raise PermissionDenied
    tweet.delete()
    messages.success(request, 'Tweet successfully deleted')
    return redirect(request.GET.get('next', '/'))
