from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView,DeleteView
from personal.models import Post, Like, Comment
from account.models import Account
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *


def home_screen_view(request, *args, **kwargs):
    user=request.user
    posts=Post.objects.all()
    post_count=Post.objects.filter(author=user)
    context ={'posts': posts, 'post_count':post_count}
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "personal/home.html", context)


def addPostView(request):
    user=request.user
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES)
        if form.is_valid():
            p=form.save()
            p.post_image=form.cleaned_data.get('post_image')
            p.author=user
            p.save()
            return redirect('home')
    context={'form': form}
    return render(request, "personal/add_post.html", context)

def editPostView(request, pk):
    post=Post.objects.get(id=pk)
    form=PostForm(instance=post)
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            p=form.save()
            p.post_image=form.cleaned_data.get('post_image')
            p.save()
            return redirect('home')
    context={'form': form}
    return render(request, "personal/edit_post.html", context)

def deletePostView(request, pk):
    post=Post.objects.get(id=pk)
    if request.method=='POST':
        post.delete()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    context={}
    return render(request, "personal/delete_post.html", context)

def like_unlike_post(request):
    user=request.user
    if request.method == 'POST':
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        account=Account.objects.get(username=user.username)

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


def save_comment(request):
    if request.method=='POST':
        body=request.POST['comment']
        post=request.POST['post']
        author=request.user
        post=Post.objects.get(pk=post)
        Comment.objects.create(
            post=post, 
            author=author,
            body=body 
        )

    return JsonResponse({'bool':True})