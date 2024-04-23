from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api.views import *

urlpatterns = [
    path('users/', ProfileListAPIView.as_view(), name='profiles'),
    path('users/<slug:username>/', ProfileAPIView.as_view(), name='profile_detail'),

    path('posts/', PostListAPIView.as_view(), name='posts'),
    path('posts/<slug:post_id>/', PostAPIView.as_view(), name='post_detail'),

    path('notify/<slug:username>/', NotificationAPIView.as_view(), name='notify_detail'),

    #path('authtoken/<slug:token>/', AdminAuthTokenView.as_view(), name='auth_detail'),
    path('sign-in/', obtain_auth_token),
    #path('upload/', UploadView.as_view(), name='api_upload'),

]