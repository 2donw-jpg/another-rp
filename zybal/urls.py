from django.urls import path, include
from zybal import views 
urlpatterns = [
    path('accounts/settings/', views.settings_view, name='settings'),
    path('accounts/login/', views.sign_in_view, name='sign_in'),
    path('accounts/register/', views.sign_up_view, name='sign_up'),
    # path('accounts/password-reset/', views.password_reset_view, name='password_reset'),
    path('accounts/logout/', views.sign_out_view, name='logout'),

    path('', views.home_view, name='home'),
    path('home/settings/', views.settings_view, name='settings'),
    path('upload', views.upload, name='upload'),
    path('search-view/', views.search_view, name='search_view'),
    path('search-user', views.search_user, name='search_user'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('follow-user/<str:username>', views.follow_user, name='follow-user'),
    path('activity/', views.activity_view, name='activity'),
]