from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse_lazy
# Create your models here.


class UserProfileManager(models.Manager):
    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass

        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True

        return added

    def isFollowing(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit=10):
        profile = user.profile
        following = profile.following.all()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user__in=following).exclude(
            id=profile.id).order_by('?')[:limit]
        return qs


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    # user.profile.following ==> users i follow
    # user.followed_by ==> user that follow me
    objects = UserProfileManager()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        return self.following.all().exclude(username=self.user.username)

    def get_follow_url(self):
        return reverse_lazy('profiles:accounts-follow', kwargs={'username': self.user.username})

    def get_absolute_url(self):
        return reverse_lazy('profiles:accounts-details', kwargs={'username': self.user.username})


def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)


post_save.connect(post_save_user, sender=settings.AUTH_USER_MODEL)
