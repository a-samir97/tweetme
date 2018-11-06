from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import TweetListAPIView, TweetCreateAPIView, RetweetAPIView, LikeAPIView, TweetDetailAPIView
app_name = 'tweets'
urlpatterns = [

    path('', TweetListAPIView.as_view()),
    path('create', TweetCreateAPIView.as_view()),  # api/tweet
    path('<int:pk>/retweet', RetweetAPIView.as_view()),
    path('<int:pk>/like', LikeAPIView.as_view()),
    path('<int:pk>', TweetDetailAPIView.as_view()),
    # path('list', tweet_list_view, name='list'),
    # path('create', create_new_tweet, name='create'),
    # path('<int:id>/update', update_tweet, name='update'),
    # path('<int:id>/delete', delete_tweet, name='delete'),
    # path('search', search_tweet, name='search_form'),
]
