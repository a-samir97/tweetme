from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views import View
from .models import UserProfile
from django.views.generic.edit import FormView, CreateView
from .forms import UserRegisterForm
# Create your views here.
User = get_user_model()


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    success_url = '/login/'
    template_name = 'user-register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)


class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwargs = 'username'

    def get_object(self):
        return get_object_or_404(User, username__iexact=self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['following'] = UserProfile.objects.isFollowing(
            self.request.user, self.get_object())
        context['recommended'] = UserProfile.objects.recommended(
            self.request.user)
        return context

# def UserDetailView(request, pk):
#     queryset = User.objects.all()
#     query = get_object_or_404(queryset, pk=pk or None)
#     print(query)
#     return render(request, 'user_detail.html')


class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(
                request.user, toggle_user)
        return redirect('profiles:accounts-details', username=username)
