from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model): #User Profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default="default_profile_image.jpg")


    def __str__(self):
        return self.user.username
    
    @property
    def followers_count(self):
        return FollowersCount.objects.filter(follower=self).count()
    @property
    def following_count(self):
        return FollowersCount.objects.filter(followed_user=self).count()


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user
    @property
    def likes_count(self):
        return LikePost.objects.filter(post=self).count()
    def user_has_liked(self, user):
        return LikePost.objects.filter(post=self, username=user).exists()


class LikePost(models.Model):
    post = models.ForeignKey(Post, related_name='post_liked', on_delete=models.CASCADE)
    username = models.ForeignKey(Profile, related_name='user_like', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)

    

class Notification(models.Model):

    NOTIFICATION_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        # Add more choices as needed
    ]

    user = models.ForeignKey(Profile, related_name='user_notified', on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(Profile, related_name='user_interacting', on_delete=models.CASCADE, null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES, null=True)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    is_read = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def str(self):
        return f"{self.notification_type} Notification for {self.user.username}"
    DEFAULT_NOTIFICATION_TYPE = 'like'  # Default value for notification_type


    