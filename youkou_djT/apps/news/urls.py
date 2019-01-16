from django.urls import path
from . import views

# app的名字
app_name = 'news'
# <a href="{% url 'new"></a>
urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.serch,name='search')
]