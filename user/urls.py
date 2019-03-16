from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('register/', views.register, name='register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('nickname_change', views.nickname_change, name='nickname_change'),
    path('bind_email', views.bind_email, name='bind_email'),   
    path('send_verification_code', views.send_verification_code, name='send_verification_code'),
    path('password_change', views.password_change, name='password_change'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
]