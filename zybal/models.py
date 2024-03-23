from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model): #User Profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default="default_profile_image.jpg")

    def __str__(self):
        return self.user.username
