from django.urls import path, include
from django.views.generic.base import RedirectView
from tweets.api.views import TweetListAPIView
app_name = 'accounts'
urlpatterns = [
    path('<username>/tweet', TweetListAPIView.as_view()),
]
