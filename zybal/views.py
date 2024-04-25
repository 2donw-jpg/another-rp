from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from zybal.models import Profile, Post, LikePost, FollowersCount, Notification
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from itertools import chain
import mimetypes


def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')  

        if password == password2:
            if User.objects.filter(email=email).exists():

                messages.info(request, 'Correo electrónico ya existe')
                return redirect('sign_up')
            elif User.objects.filter(username=username).exists():

                messages.info(request, 'Usuario ya existe') 
                return redirect('sign_up')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Profile.objects.create(user=user, id=user.pk)
                login(request, user)
                return redirect('settings')
        else:
            messages.info(request, 'Contraseñas no coinciden')
            return redirect('sign_up')

    return render(request, 'accounts/auth-signup.html')

def sign_in_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usuario y/o contraseña incorrecta')
            return redirect('sign_in')
    else:
        return render(request, 'accounts/auth-signin.html')

@login_required(login_url='sign_in')
def sign_out_view(request):
    logout(request)
    return redirect('sign_in')

@login_required(login_url='sign_in')
def settings_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        print("Does the user put an image?")
        if 'image' in request.FILES:
            profile.profile_image = request.FILES.get('image')
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        profile.bio = request.POST.get('bio', profile.bio)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()
        
        return redirect('home')

    return render(request, 'pages/settings.html', {'profile': profile})

#TODO: Only get the feed of users following
@login_required(login_url='sign_in')
def home_view(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().order_by('-created_at')
    followers = profile.followers_data
    following = profile.following_data

    notifications = Notification.objects.filter(user__id=profile.id).order_by('-created_at')

    for post in posts:
        post.user_has_liked = post.user_has_liked(profile)

    context = {
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'notifications': notifications,
    }
    return render(request, 'pages/index.html', context)



@login_required(login_url='sign_in')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')



#TODO Make a search html page
@login_required(login_url='sign_in')
def search_user(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    notifications = Notification.objects.filter(user__id=profile.id).order_by('-created_at')
    username = request.POST.get('search')
    context = {
        'notifications': notifications,
        'profile': profile,
        'profile_search': username,
        'notifications': notifications,
    }
    return render(request, 'pages/search.html', context)

@login_required(login_url='signin')
def search_view(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    notifications = Notification.objects.filter(user__id=profile.id).order_by('-created_at')    
    if request.method == 'POST':
        username_profile_list = []
        
        search_username = request.POST.get('search')
        matching_users = User.objects.filter(username__icontains=search_username)
        
        for user_obj in matching_users:
            matching_profiles = Profile.objects.filter(user=user_obj)
            username_profile_list.extend(matching_profiles)
    else:
        username_profile_list = []  

    return render(request, 'pages/search.html', {'profile': profile, 'username_profile_list': username_profile_list, 'notifications': notifications,})

#TODO: It requieres to send an image as mandatory
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        profile = Profile.objects.get(user=request.user)
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption', '')

        if not image: 
            image = None

        new_post = Post.objects.create(user=profile, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    return redirect('home')

@login_required(login_url='signin')
def profile_view(request,username):
    profile = Profile.objects.get(user=request.user)
    profile_searched = Profile.objects.get(user__username=username)
    posts = Post.objects.filter(user__user__username = username).order_by('-created_at')
    notifications = Notification.objects.filter(user__id=profile.id).order_by('-created_at')
    following = profile.following_data
    for post in posts:
        post.user_has_liked = post.user_has_liked(profile)

    context = {
        'profile': profile,
        'posts': posts,
        'profile_searched':profile_searched,
        'following':following,
        'notifications': notifications,
    }

    return render(request, 'pages/profile.html', context)



def serve_image(request, image_path):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    content_type, _ = mimetypes.guess_type(image_full_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    return FileResponse(open(image_full_path, 'rb'), content_type=content_type)

    
@login_required(login_url='signin')
def like_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=profile).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=profile)
        new_like.save()

        new_notification = Notification.objects.create(user=post.user,sender=profile,notification_type='like',target_post_id=post_id)
        new_notification.save()
        return redirect('home')
    else:
        new_notification = Notification.objects.create(user=post.user,sender=profile,notification_type='dislike',target_post_id=post_id)
        new_notification.save()
        like_filter.delete()
        return redirect('home')


@login_required(login_url='signin')
def follow_user(request, username):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_searched = Profile.objects.get(user__username=username)

    is_follower = FollowersCount.objects.filter(follower=profile, followed_user=profile_searched).first()

    if is_follower == None:
        follower_created = FollowersCount.objects.create(follower=profile, followed_user=profile_searched)
        follower_created.save()

        new_notification = Notification.objects.create(user=profile_searched,sender=profile,notification_type='follow')
        new_notification.save()
        return redirect('profile', username=username)
    else:
        is_follower.delete()
        new_notification = Notification.objects.create(user=profile_searched,sender=profile,notification_type='unfollow')
        new_notification.save()
        return redirect('profile', username=username)


#TODO: Make it so it only gets the notifications of the user connected
def activity_view(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().order_by('-created_at')

    notifications = Notification.objects.filter(user__id=profile.id).order_by('-created_at')
    context = {
        'profile': profile,
        'notifications': notifications,
    }
    return render(request, 'pages/activity.html', context)