from django.contrib import admin
from django.urls import path
from . import views
# http://127.0.0.1:8000/user/register
urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.profile, name='profile')

]
