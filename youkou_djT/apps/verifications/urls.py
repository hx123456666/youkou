# from django.urls import path
# from . import views
#
# path('/image_code/<uuid:image_code_id>/',views.ImageCode.as_view(),name='')
from django.urls import path,re_path
from . import views

app_name="verification"
urlpatterns = [
    # re_path(r'^image_codes/(?P<image_code_id>[\w-]+)/$', view=views.ImageCodeView.as_view(), name="image_code"),
    # image_code_id为uuid格式
    path('image_codes/<uuid:image_code_id>/',views.ImageCode.as_view(),name='inage_codes'),
    re_path('usernames/(?P<username>\w{5,20})/',views.CheckUsernameView.as_view(),name='check_username'),
]