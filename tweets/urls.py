from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import (tweet_details_view,
                    tweet_list_view,
                    create_new_tweet,
                    update_tweet,
                    delete_tweet,
                    RetweetView
                    )
app_name = 'tweets'
urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<int:id>', tweet_details_view, name='details'),
    path('<int:pk>/retweet', RetweetView.as_view(), name='retweet'),
    path('list', tweet_list_view, name='list'),
    path('create', create_new_tweet, name='create'),
    path('<int:id>/update', update_tweet, name='update'),
    path('<int:id>/delete', delete_tweet, name='delete'),
    path('search', tweet_list_view, name='search'),

]
