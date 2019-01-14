from django.urls import path
# from .views import index, search
from . import views
# app的名字
app_name = 'news'
# reverse('news:index')

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
]