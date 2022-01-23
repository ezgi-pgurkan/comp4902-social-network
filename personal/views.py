from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import ListView, DetailView
from personal.models import Post
from django.urls import reverse, reverse_lazy

#from personal.models import Post



def home_screen_view(request, *args, **kwargs):
	posts=Post.objects.all()
	context ={'posts': posts}
	if not request.user.is_authenticated:
		return redirect('login')
	return render(request, "personal/home.html", context)


def postDetailView(request, pk):
	post=Post.objects.get(pk=pk)
	context ={'post': post}
	return render(request, "personal/post_details.html", context)