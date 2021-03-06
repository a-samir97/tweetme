import re
from django.db.models.signals import post_save
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
# Create your models here.


# validation
def validate_content(value):
    content = value
    if content == 'abc':
        raise ValidationError("Content can not ABC")
    return value


class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):

        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj
        qs = self.get_queryset().filter(user=user, parent=og_parent)
        if qs.exists():
            return None
        obj = self.model(
            parent=og_parent,
            user=user,
            content=parent_obj.content,
            reply=False,
        )
        obj.save()

        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)

        return is_liked


class Tweet(models.Model):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.CharField(max_length=140, validators=[validate_content])
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name='is a reply ?', default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    def __str__(self):
        return (self.content)

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-timestamp"]

    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_children(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        qs_parent = Tweet.objects.filter(pk=parent.pk)
        return (qs | qs_parent)


def tweet_save(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        m = re.search(user_regex, instance.content)
        if m:
            username = m.group("username")
            print(username)
            # send notification to user here
        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        m = re.search(hash_regex, instance.content)
        if m:
            hashtag = m.group("hashtag")
            print(hashtag)


post_save.connect(tweet_save, sender=Tweet)
