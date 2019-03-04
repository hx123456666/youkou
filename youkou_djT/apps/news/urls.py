from django.urls import path
from . import views

# app的名字
app_name = 'news'
# <a href="{% url 'new"></a>
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('search/',views.SerchView.as_view(),name='search'),
    path('news/',views.NewsListView.as_view(),name='news_list'),
    path('news/banners/',views.NewsBanner.as_view(),name='news_banner'),
    path('news/<int:news_id>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:news_id>/comments/', views.NewsCommentView.as_view(), name='news_comment'),
]