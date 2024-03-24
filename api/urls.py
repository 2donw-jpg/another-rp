from django.urls import path
from api.views import ProfileAPIView, ProfileListAPIView

urlpatterns = [
    path('users/', ProfileListAPIView.as_view(), name='profiles'),
    path('users/<int:user_id>/', ProfileAPIView.as_view(), name='profile_detail'),
]