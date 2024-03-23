from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from zybal.models import Profile
from django.contrib import messages
from django.http import HttpResponse


def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']  # We use doble password for validation
        password2 = request.POST['password2']  

        if password == password2:
            if User.objects.filter(email=email).exists():
                # Make a notification that the email is already taken
                messages.info(request, 'Email already used')
                return redirect('sign_up_view')
            elif User.objects.filter(username=username).exists():
                # Make a notification that the username is already taken
                messages.info(request, 'Username already used') 
                return redirect('sign_up_view')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                new_profile = Profile.objects.create(user=user, id_user=user.pk)
                return redirect('sign_in_view')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('sign_up_view')

    return render(request, 'accounts/auth-signup.html')


def sign_in_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'User and/or Password incorrect')
            return redirect('sign_in_view')
    else:
        return render(request, 'accounts/auth-signin.html')


def sign_out_view(request):
    logout()
    return render(request, 'accounts/auth-signin.html')




def password_reset(request):

    return render(request, 'accounts/auth-reset.html')



def home_view(request):
    return render(request,'pages/index.html')