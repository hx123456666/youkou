from django.urls import path
from . import views

# app的名字
app_name = 'user'

urlpatterns = [
    # path('login/',views.login,name='login'),
    # path('register/',views.register,name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
]