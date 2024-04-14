from django.urls import path, include
from zybal.views import profile_view,upload_view, settings_view, sign_in_view, sign_up_view,sign_out_view, password_reset_view, home_view, like_post_view
urlpatterns = [
    path('accounts/settings/', settings_view, name='settings'),
    path('accounts/login/', sign_in_view, name='sign_in'),
    path('accounts/register/', sign_up_view, name='sign_up'),
    path('accounts/password-reset/', password_reset_view, name='password_reset'),
    path('accounts/logout/', sign_out_view, name='logout'),

    path('', home_view, name='home'),
    path('home/settings/', settings_view, name='settings'),
    path('upload', upload_view, name='upload'),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:pk>/', profile_view, name='profile_detail'),
    path('like-post', like_post_view, name='like-post'),
]