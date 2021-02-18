from django.contrib.auth import login, logout
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from user.forms import RegistrationForm
from user.models import User
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/user.html")


def user_registration(request):
    registration_form = RegistrationForm()
    if request.method == 'POST':
        print(request.POST)
        registration_form: RegistrationForm = RegistrationForm(request.POST, files=request.FILES)
        print(registration_form.errors)
        if registration_form.is_valid():
            customer: User = registration_form.save(commit=False)
            customer.status = User.Status.customer
            customer.save()
            return redirect('user:user_login')

    return render(request, template_name='user/registration.html', context={
        'form': registration_form
    })


def user_login(request):
    if request.user.is_authenticated:
        return render(request, template_name="user/user.html")
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form is not None:
            login(request, form.get_user())
            return render(request, template_name="user/user.html")
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, template_name="user/login.html", context={
        'form': form
    })


def user_logout(request):
    logout(request)
    return render(request, template_name="user/login.html", context={
        "message": "Logged out."
    })
