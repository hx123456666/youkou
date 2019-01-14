from django.urls import path
from .views import index


app_name='doc'
urlpatterns=[
    path('', index, name='index'),
]