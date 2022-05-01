from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from models.models import Ticket


from .forms import *


@login_required(login_url='login')
def profile_page(request):

    form = CustomUserForm(request.POST or None,
                          instance=request.user.customuser)

    tickets: list[Ticket] = Ticket.objects.filter(user=request.user.id)

    if (request.method == 'POST'):
        if (form.is_valid()):
            form.save()
            messages.success(request, "Profile was updated!")

    return render(request, 'accounts/profile.html', {
        'form': form,
        'tickets': tickets,
    })


def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') or 'home')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'accounts/login.html')


def register_page(request):
    form = RegisterForm(request.POST or None)

    if (request.method == 'POST'):
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Account was created for " + username)
            return redirect('login')

    return render(request, 'accounts/register.html', {
        'form': form
    })


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
