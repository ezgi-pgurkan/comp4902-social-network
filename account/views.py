from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfileForm
from account.models import Account, Profile
from personal.models import Post, Like, Comment
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy

def register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated: 
        return HttpResponse("You are already authenticated as " + str(user.email))
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination: #if destination != None
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect("login")

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated: 
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def account_view(request, *args, **kwargs):
    """
    - Logic here is kind of tricky
        is_self (boolean)
            is_friend (boolean)
                -1: NO_REQUEST_SENT
                0: THEM_SENT_TO_YOU
                1: YOU_SENT_TO_THEM
    """

    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/account.html", context)

def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(Q(email__icontains=search_query)|Q(username__icontains=search_query)).distinct()
            user = request.user
            accounts = [] # [(account1, True), (account2, False), ...]
            for account in search_results:
                accounts.append((account, False))
            context['accounts'] = accounts
                
    return render(request, "account/search_results.html", context)



def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            account.profile_image.delete()
            form.save()
            return redirect("account:view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                initial={
                    "id": account.pk,
                    "email": account.email, 
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                    "id": account.pk,
                    "email": account.email, 
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context)

@receiver([post_save], sender=Account)
def add_user_data(sender, **kwargs):
    user = kwargs.get('instance')

    try:
        profile, profile_created = Profile.objects.get_or_create(profile=user,
          )
    except MultipleObjectsReturned:
        pass


def profile_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
        posts=Post.objects.filter(author=user_id)
        info=Profile.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL
        context['posts'] = posts
        context['account'] = account
        context['info'] = info
    return render(request, "account/profile_page.html", context)

def editProfileView(request, *args, **kwargs):
    user_id = kwargs.get("user_id")
    info=Profile.objects.get(profile=user_id)
    form=ProfileForm(instance=info)
    if request.method=='POST':
        form=ProfileForm(request.POST, instance=info)
        if form.is_valid():
            p=form.save()
            p.save()
            return redirect('home')  
    context={'form': form}
    return render(request, "account/edit_profile.html", context)
