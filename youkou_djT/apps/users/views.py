import json
import logging

from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.views import View


from .models import Users
from .forms import RegisterForm, LoginForm
from utils.json_fun import to_json_data
from utils.res_code import Code,error_map

# Create your views here.

logger = logging.getLogger('django')
# def login(request):
#     return render(request,'users/login.html')

# def register(request):
#     return render(request,'users/register.html')

class LoginView(View):
    """
    POST:
    1、创建一个类视图
    2、创建一个GET方法
    3、创建一个POST方法
    4、获取前端传过来的参数
    5、校验参数
    6、如果有记住的选择的话，将用户登录信息保存到redis
    6、将结果返回给前端
    """
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        """

        :param request:
        :return:
        """
        try:
            json_data = request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
            dict_data = json.loads(json_data.decode('utf-8')) # 没有解码，会产生bug
        except Exception as e:
            logger.info("错误信息，\n{}".format(e))
        # 3、校验参数
        form = LoginForm(data=dict_data,request=request)

        # 4、返回前端
        if form.is_valid():
            return to_json_data(errmsg="恭喜您，登录成功！")
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get("message"))
            err_msg_str = "/".join(err_msg_list) # 拼接一个错误信息为字符串
            return to_json_data(errno=Code.PARAMERR,errmsg=err_msg_str)


# 1、创建一个类视图
class RegisterView(View):
    """
    handle register
    1、创建一个类视图
    2、创建一个GET方法
    3、创建一个POST方法
    4、获取前端传过来的参数
    5、校验参数
    6、将用户信息保存到数据库
    7、将结果返回给前端
    """
    #     2、创建一个GET方法
    def get(self,request):
        """
        :param request:
        :return: GET: users/register.html/
        """
        """处理GET请求,返回注册页面"""
        return render(request,'users/register.html')

    #     3、创建一个POST方法
    def post(self,request):
        """

        :param request:
        :return: POST:
        """
        """处理POST请求，实现注册逻辑"""

        #     4、获取前端传过来的参数

        try:
            json_data = request.body
            if not json_data: # 判断参数是否合法
                return to_json_data(errno=Code.PARAMERR, errmsg = error_map[Code.PARAMERR])
            dict_data = json.loads(json_data.decode('utf-8'))
        except Exception as e:
            logger.info("错误信息：\n{}".format(e))
            return to_json_data(errno=Code.UNKOWNERR,errmsg=error_map[Code.UNKOWNERR])

        # 将json 转化为dict
        # dict_data = json.loads(json_data.decode('utf-8'))

        # 3、校验参数
        form = RegisterForm(data=dict_data)
        if form.is_valid():
            # 获取username password Mobile 关键参数
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            mobile = form.cleaned_data.get("mobile")

            user = Users.objects.create_user(username=username,password=password,mobile=mobile)
            login(request,user)
            return to_json_data(errmsg="恭喜您，注册成功！")


        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get("message"))
            err_msg_str = "/".join(err_msg_list)

            return to_json_data(errno=Code.PARAMERR,errmsg=err_msg_str)


class LogoutView(View):
    """

    """
    def get(self,request):
        logout(request)
        return redirect(reverse('user:login'))
