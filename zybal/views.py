from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import authenticate, login, logout
from zybal.models import Profile, Post
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import os
import mimetypes
import random
import string


#TODO When successfully sign up send it to settings
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







#TODO Notify user when failed login
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






#Sign Out
@login_required(login_url='sign_in')
def sign_out_view(request):
    logout(request)
    return redirect('sign_in')




#TODO apply the SMTP and the verification method
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







#FIXME This doesn't store the user attributes: first_name and last_name
@login_required(login_url='sign_in')
def settings_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        # Check if 'image' file is uploaded
        if 'image' in request.FILES:
            profile.profile_image = request.FILES['image']
        

        profile.user.first_name = request.POST.get('first_name', user.first_name)
        profile.user.last_name = request.POST.get('last_name', user.last_name)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()
        return redirect('home')

    return render(request, 'pages/settings.html', {'profile': profile})


    

#TODO apply the followers/following values from the user
@login_required(login_url='sign_in')
def home_view(request):
    profile = Profile.objects.get(user=request.user)
    # Obtener el número de seguidores y siguiendo (puedes implementar lógica real aquí)
    followers_count = 15
    following_count = 15


    context = {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'pages/index.html', context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption', '')

        if not image: 
            image = None

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('home')

    
    return redirect('home')





def serve_image(request, image_path):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    content_type, _ = mimetypes.guess_type(image_full_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    return FileResponse(open(image_full_path, 'rb'), content_type=content_type)

