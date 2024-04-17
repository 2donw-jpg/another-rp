from django.urls import path
from api.views import ProfileAPIView, ProfileListAPIView, PostListAPIView, PostAPIView, NotificationAPIView

urlpatterns = [
    # API endpoints for profiles
    path('users/', ProfileListAPIView.as_view(), name='profiles'),
    path('users/<int:user_id>/', ProfileAPIView.as_view(), name='profile_detail'),

    # API endpoints for posts
    path('posts/', PostListAPIView.as_view(), name='posts'),
    path('posts/<slug:post_id>/', PostAPIView.as_view(), name='post_detail'),

    # API endpoint for notifications
    path('notify/<int:user>/', NotificationAPIView.as_view(), name='notify_detail'),

]
