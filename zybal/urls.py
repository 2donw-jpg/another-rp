from django.urls import path, include
from zybal.views import follow_user_view,activity_view,profile_view,upload_view, settings_view, sign_in_view, sign_up_view,sign_out_view, password_reset_view, home_view, like_post_view
urlpatterns = [
    path('accounts/settings/', settings_view, name='settings'),
    path('accounts/login/', sign_in_view, name='sign_in'),
    path('accounts/register/', sign_up_view, name='sign_up'),
    path('accounts/password-reset/', password_reset_view, name='password_reset'),
    path('accounts/logout/', sign_out_view, name='logout'),

    path('', home_view, name='home'),
    path('home/settings/', settings_view, name='settings'),
    path('upload', upload_view, name='upload'),
    path('profile/<str:username>/', profile_view, name='profile_detail'),
    path('like-post', like_post_view, name='like-post'),
    path('follow-user/<str:username>', follow_user_view, name='follow-user'),
    path('activity/', activity_view, name='activity'),

    



]