from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


from .forms import *


def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'accounts/login.html')


def register_page(request):

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Account was created for " + username)
            return redirect('/account/login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/account/login')
