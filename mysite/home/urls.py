from django.urls import path
from . import views

urlpatterns = [
path('', views.home , name="home"),
path('contact/', views.contact , name="contact"),
path('about/', views.about , name="about"),
path('search', views.search , name="search"),
path('signup/', views.handleSignup,name='handleSignup'),
path('login/', views.loginhandle, name='loginhandle'),
path('logout/', views.userlogout,name='userlogout'),
path('viewprofile/', views.viewprofile,name='viewprofile'),
path('change_password/', views.change_password,name='change_password'),




]