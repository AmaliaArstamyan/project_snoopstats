from django.urls import path
from accounts.views import register, user_login
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
