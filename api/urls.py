from django.urls import path
from api.views import ProfileAPIView, ProfileListAPIView, PostListAPIView, PostAPIView, NotificationAPIView

urlpatterns = [
    path('users/', ProfileListAPIView.as_view(), name='profiles'),
    path('users/<slug:username>/', ProfileAPIView.as_view(), name='profile_detail'),

    path('posts/', PostListAPIView.as_view(), name='posts'),
    path('posts/<slug:post_id>/', PostAPIView.as_view(), name='post_detail'),

    path('notify/<slug:username>/', NotificationAPIView.as_view(), name='notify_detail'),
]