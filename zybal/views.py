from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from zybal.models import Profile
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
import dev.settings as dev_settings
import os, mimetypes, random, string

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings



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


    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)  # Assuming you have a User model
        if user is not None:

            return render(request, 'accounts/auth-verification.html')
        else:
            return HttpResponse('No user found with that email address.')
    
    return render(request, 'accounts/auth-reset.html')
"""
        # Generate a random token
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Save token to the database
        #password_reset_token = PasswordResetToken.objects.create(user=user, token=token)
        
        # Send email with token
        send_mail(
            'Password Reset',  # Subject
            f'Click the following link to reset your password: {settings.BASE_URL}/reset_password/{token}',  # Message
            'your_email@example.com',  # Sender email
            [email],  # Recipient email
            fail_silently=False
        )
        
        return HttpResponse('Password reset email sent successfully.')
"""
    


@login_required(login_url='sign_in')
def home_view(request):
    profile = Profile.objects.get(user=request.user)
    # Obtener el número de seguidores y siguiendo (puedes implementar lógica real aquí)
    followers_count = 14
    following_count = 1
    context = {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'pages/index.html', context)

def serve_image(request, image_path):

    image_full_path = os.path.join(dev_settings.MEDIA_ROOT, image_path)
    content_type, _ = mimetypes.guess_type(image_full_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    return FileResponse(open(image_full_path, 'rb'), content_type=content_type)

