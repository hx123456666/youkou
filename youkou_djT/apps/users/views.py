from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

# def login(request):
#     return render(request,'users/login.html')

# def register(request):
#     return render(request,'users/register.html')

class LoginView(View):
    """handle Login"""
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        return HttpResponse("这里实现登录逻辑")


class RegisterView(View):
    """handle register"""

    def get(self,request):
        """处理GET请求,返回注册页面"""
        return render(request,'users/register.html')
    def post(self,request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse("这里实现注册逻辑")


