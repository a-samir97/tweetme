from django.shortcuts import render
from django.views import View
from .models import Hashtag
# Create your views here.


class HashtagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = Hashtag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtag_view.html', {'obj': obj})
