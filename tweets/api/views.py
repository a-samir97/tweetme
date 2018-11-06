from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsPagination
from accounts.models import UserProfile


class LikeAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = "Not Allowed"
        if request.user.is_authenticated:
            liked = Tweet.objects.like_toggle(
                request.user, tweet_qs.first())
            return Response({'liked': liked})
        return Response({'message': message}, status=400)


class RetweetAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = "Not Allowed"

        if tweet_qs.exists() and tweet_qs.count() == 1:
            if request.user.is_authenticated:
                new_tweet = Tweet.objects.retweet(
                    request.user, tweet_qs.first())

                if new_tweet is not None:
                    data = TweetModelSerializer(new_tweet).data
                    return Response(data)

                messgae = 'Cannot retweet the same in one day'
        return Response({'message': message}, status=400)


class TweetDetailAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get('pk')
        qs = Tweet.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(
                select={'parent_id_null': 'parent_id IS NULL'})
        return qs.order_by("-parent_id_null", "-timestamp")


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetListAPIView, self).get_serializer_context(
            *args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get('username')
        if requested_user:
            qs = Tweet.objects.filter(
                user__username=requested_user).order_by("-timestamp")
            query = self.request.GET.get('search', None)
            if query is not None:
                qs = qs.filter(Q(content__icontains=query) |
                               Q(user__username__icontains=query))
            return qs

        else:
            my_followers = self.request.user.profile.get_following()

            qs1 = Tweet.objects.filter(
                user__in=my_followers).order_by("-timestamp")
            qs2 = Tweet.objects.filter(user=self.request.user)
            qs = (qs1 | qs2).distinct()
            query = self.request.GET.get('search', None)
            if query is not None:
                qs = qs.filter(Q(content__icontains=query) |
                               Q(user__username__icontains=query))
            return qs
