from django.urls import path
from . import views

# app的名字
app_name = 'one'

urlpatterns = [
    path('',views.index,name='index'),
    # print('one/<str:username>/',views.Delete,name='delete')
]