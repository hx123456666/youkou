from django.urls import path
from . import views

# app的名字
app_name = 'user'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register')
]