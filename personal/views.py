from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import ListView, DetailView
from personal.models import Post

#from personal.models import Post



def home_screen_view(request, *args, **kwargs):
	posts=Post.objects.all()
	context ={'posts': posts}
	if not request.user.is_authenticated:
				return redirect('login')
	return render(request, "personal/home.html", context)


def addCommentView(request, restname):
    rest = get_object_or_404(Restaurant, restname=restname)
    customer=request.user.customer
    
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review= Review.objects.create(author=customer, restaurant=rest)
            review.body=form.cleaned_data.get('body')
            review.save()  
            return redirect('store', restname) 

    context = {'form':form, 'rest':rest, 'customer':customer}
    return render(request, 'store/add_review.html', context)

