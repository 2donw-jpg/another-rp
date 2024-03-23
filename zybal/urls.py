from django.urls import path, include
from zybal.views import sign_in_view, sign_up_view, password_reset, home_view
urlpatterns = [
    path('', sign_in_view, name='login'),
    path('accounts/login/', sign_in_view, name='sign_in_view'),
    path('accounts/register/', sign_up_view, name='sign_up_view'),
    path('accounts/password-reset/', password_reset, name='password_reset'),

    path('home', home_view, name='home'),
]