from django.urls import path
from . import views

# app的名字
app_name = 'doc'

urlpatterns = [
    path('',views.index,name='index')
]