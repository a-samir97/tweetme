from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import UserDetailView, UserFollowView
app_name = 'accounts'
urlpatterns = [
    #path('', RedirectView.as_view(url='/')),
    #path('<int:pk>', UserDetailView.as_view(), name='accounts-details'),
    path('<slug:username>', UserDetailView.as_view(), name='accounts-details'),
    path('<slug:username>/follow', UserFollowView.as_view(), name='accounts-follow'),
    #path('list', tweet_list_view, name='list'),
    #path('create', create_new_tweet, name='create'),
    #path('<int:id>/update', update_tweet, name='update'),
    #path('<int:id>/delete', delete_tweet, name='delete'),
    #path('search', tweet_list_view, name='search'),

]
