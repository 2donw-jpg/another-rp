from django.urls import path, include
<<<<<<< HEAD
from zybal.views import *
=======
from zybal import views
>>>>>>> 1c4e86937ab64145e7f194be99c6d7ffc44fcb9a
urlpatterns = [
    path('accounts/settings/', views.settings_view, name='settings'),
    path('accounts/login/', views.sign_in_view, name='sign_in'),
    path('accounts/register/', views.sign_up_view, name='sign_up'),
    #path('accounts/password-reset/', views.password_reset_view, name='password_reset'),
    path('accounts/logout/', views.sign_out_view, name='logout'),

    path('', views.home_view, name='home'),
    path('home/settings/', views.settings_view, name='settings'),
    path('upload', views.upload, name='upload'),
    path('search_user', views.search_user, name='search_user'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('follow-user/<str:username>', views.follow_user, name='follow-user'),
    path('activity/', views.activity_view, name='activity'),

    

    



<<<<<<< HEAD
    path('', home_view, name='home'),
    path('home/settings/', settings_view, name='settings'),
    path('upload', upload_view, name='upload'),
    path('search-user/<str:username>/', search_view, name='search_user'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('like-post', like_post_view, name='like-post'),
    path('follow-user/<str:username>', follow_user_view, name='follow-user'),
    path('activity/', activity_view, name='activity'),
=======
>>>>>>> 1c4e86937ab64145e7f194be99c6d7ffc44fcb9a
]