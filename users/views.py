from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Connections
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.models import Post


def profile(request, slug):
    followers = Connections.objects.all().filter(follower=request.user)
    followings = Connections.objects.all().filter(following=request.user)

    print(followers)
    print(followings)

    posts = Post.objects.all().filter(author=request.user)
    return render(request, 'users/profile.html', {'followers': followers, 'followings': followings, 'posts': posts})



class ProfileCreateView(LoginRequiredMixin, CreateView):
	model = Profile
	fields = ['first_name', 'last_name', 'is_male', 'is_female', 'image', 'background']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'is_male', 'is_female', 'image', 'background']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def followers(request, slug):
	followers = Connections.objects.all().filter(following=request.user)
	return render(request, 'users/followers.html', {'followers':followers})


def followings(request, slug):
	followings = Connections.objects.all().filter(follower=request.user)
	return render(request, 'users/followings.html', {'followings':followings})