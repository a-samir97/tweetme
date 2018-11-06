from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import View
from .models import Tweet
from .forms import TweetModelForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q


# Create your views here.
# Retrive Data
class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated:
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect(tweet.get_absolute_url())


def tweet_details_view(request, id=id):
    # Get Data From Database
    # obj = Tweet.objects.get(id=id)
    obj = get_object_or_404(Tweet, id=id)
    context = {
        'object': obj
    }
    return render(request, 'detail_view.html', context)


def tweet_list_view(request):
    # Get All Data in Database ==> which means to get all tweets in database
    form = TweetModelForm(request.POST or None)
    context = {}
    tweet_search = request.GET.get("search" or None)
    if tweet_search and request.method == "GET":
        status = Tweet.objects.all().filter(content__icontains=tweet_search)
        context.update({'object_list': status, 'form': form})
        return render(request, 'search.html', context)
    else:
        queryset = Tweet.objects.all()
        context.update({'object_list': queryset, 'form': form})
        return render(request, 'list_view.html', context)


def create_new_tweet(request):
    form = TweetModelForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('tweet:list')
        else:
            con = {
                'error': 'you must login first'
            }
            return render(request, 'error.html', con)

    context = {
        'form': form
    }

    return render(request, 'create_view.html', context)


def delete_tweet(request, id):
    deleted_tweet = get_object_or_404(Tweet, id=id)
    if request.method == 'POST' and request.user.is_authenticated:
        deleted_tweet.delete()
        return redirect('tweet:list')
        # reverse('tweet:list')
    context = {
        'tweet': deleted_tweet,
    }
    return render(request, 'delete_confirm.html', context)


def update_tweet(request, id):
    tweet = get_object_or_404(Tweet, id=id)
    if request.method == 'POST':
        form = TweetModelForm(request.POST, instance=tweet)
        if form.is_valid():
            updated_form = form.save(commit=False)
            if request.user == updated_form.user:
                # updated_form.user = request.user
                updated_form.save()
                return redirect('tweet:list')
    else:
        form = TweetModelForm(instance=tweet)

    context = {
        'form': form
    }
    return render(request, 'update_view.html', context)
