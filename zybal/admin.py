from django.contrib import admin
from .models import Profile, LikePost

# Register your models here.
admin.site.register(Profile)
admin.site.register(LikePost)