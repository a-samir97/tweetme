"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from hashtags.views import HashtagView
from .views import SearchView
from hashtags.api.views import TagTweetAPIView
from django.contrib.auth import views as auth_views
from accounts.views import UserRegisterView
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    re_path(r'^tags/(?P<hashtag>.*)/$',
            HashtagView.as_view(), name='hashtag'),
    re_path(r'^api/tags/(?P<hashtag>.*)/$',
            TagTweetAPIView.as_view(), name='hashtag-api'),
    path('admin/', admin.site.urls),
    path('tweets/', include('tweets.urls', namespace='tweet')),
    path('', include('accounts.urls', namespace='profiles')),
    path('api/tweets/', include('tweets.api.urls', namespace='tweet_api')),
    path('api/', include('accounts.api.urls', namespace='profiles_api')),
    path('', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
