from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model): #User Profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default="default_profile_image.jpg")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.ForeignKey(Profile, related_name='post_liked', on_delete=models.CASCADE)
    username = models.ForeignKey(Profile, related_name='user_like', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)

    

class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


    