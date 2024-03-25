from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from zybal.models import Profile
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
import dev.settings as settings
import os, mimetypes



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
                return redirect('sign_up')
            elif User.objects.filter(username=username).exists():
                # Make a notification that the username is already taken
                messages.info(request, 'Username already used') 
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                new_profile = Profile.objects.create(user=user, id_user=user.pk)
                
                return redirect('sign_in')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('sign_up')

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
            return redirect('sign_in')
    else:
        return render(request, 'accounts/auth-signin.html')


@login_required(login_url='sign_in')
def sign_out_view(request):
    logout(request)
    return render(request, 'accounts/auth-signin.html')


@login_required(login_url='sign_in')
def settings_view(request):
    logout(request)
    return render(request, 'pages/settings.html')


def password_reset_view(request):
    return render(request, 'accounts/auth-reset.html')


@login_required(login_url='sign_in')
def home_view(request):
    return render(request, 'pages/index.html')

def serve_image(request, image_path):

    image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    content_type, _ = mimetypes.guess_type(image_full_path)
    if content_type is None:
        content_type = 'application/octet-stream'  # Default to binary file if type cannot be determined
    return FileResponse(open(image_full_path, 'rb'), content_type=content_type)

