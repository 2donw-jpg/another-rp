from django.urls import path, include
from zybal.views import *
urlpatterns = [
    path('accounts/settings/', settings_view, name='settings'),
    path('accounts/login/', sign_in_view, name='sign_in'),
    path('accounts/register/', sign_up_view, name='sign_up'),
    path('accounts/password-reset/', password_reset_view, name='password_reset'),
    path('accounts/logout/', sign_out_view, name='logout'),

    path('', home_view, name='home'),
    path('home/settings/', settings_view, name='settings'),
    path('upload', upload_view, name='upload'),
    path('search-user/<str:username>/', search_view, name='search_user'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('like-post', like_post_view, name='like-post'),
    path('follow-user/<str:username>', follow_user_view, name='follow-user'),
    path('activity/', activity_view, name='activity'),
]