from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView
from personal.models import Post, Like
from account.models import Account
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *



def home_screen_view(request, *args, **kwargs):
    user=request.user
    posts=Post.objects.all()
    account=Account.objects.get(username=user)
    context ={'posts': posts, 'account':account}
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "personal/home.html", context)


def postDetailView(request, pk):
    post=Post.objects.get(pk=pk)
    context ={'post': post}
    return render(request, "personal/post_details.html", context)

def addPostView(request):
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES)
        if form.is_valid():
            p=form.save()
            p.post_image=form.cleaned_data.get('post_image')
            p.save()
            return redirect('home')
    context={'form': form}
    return render(request, "personal/add_post.html", context)

def like_unlike_post(request):
    user=request.user
    if request.method == 'POST':
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        account=Account.objects.get(username=user)

        if account in post_obj.liked.all():
            post_obj.liked.remove(account)
        else:
            post_obj.liked.add(account)

        like, created = Like.objects.get_or_create(user=account, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value == 'Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()


        data = {
        'value':like.value,
        'likes':post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)

    return redirect ('home')


