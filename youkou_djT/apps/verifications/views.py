# 第一部分导入的是Python（系统的）的模块
import logging

# 第二部分导入的是Django内的模块
# from django.shortcuts import render,redirect,reverse
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse, JsonResponse

# 第三部分导入的是我们自己写的模块
from utils.captcha.captcha import captcha
from . import constants
from apps.users.models import Users
from utils.json_fun import to_json_data


# 导入日记器
logger = logging.getLogger('django')


# 1、创建一个ImageCode类视图
class ImageCode(View):
    """
    define image verification View
    /image_code/<uuid:image_code_id>/
    1、创建一个ImageCode类视图
    2、从前端获取参数uuid==>def get(self,request,image_code_id):
    3、生成验证码文本和验证图片
    4、建立redis，并且将图片验证码保存到redis
    5、把验证码图片返回前端
    """

    # 2、从前端获取参数uuid==>def get(self,request,image_code_id):
    def get(self,request,image_code_id):
        # 3、生成验证码文本和验证图片
        text,image = captcha.generate_captcha()

        # 确保setting.py 文件中有配置redis CACHE
        # Redis原生指令参考 http://redisdoc.com/index.html
        # Redis python客户端 方法参考 http://redis-py.readthedocs.io/en/latest/#indices-and-tables

        # 4、建立redis，并且将图片验证码保存到redis
        con_redis = get_redis_connection(alias='verify_codes')  # 建立连接指定别名为verify_code的redis库

        img_key = "img_{}".format(image_code_id).encode('utf-8') # 设置redis中key名字： img_123e4567-e89b-12d3-a456-426655440000

        # 将图片验证码的key和验证码文本保存到redis中，并设置过期时间
        con_redis.setex(img_key,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        logger.info('Image code: {}'.format(text))

        # 5、把验证码图片返回前端
        return HttpResponse(content=image,content_type="images/jpg")


# 1、创建一个类视图
class CheckUsernameView(View):
    """
    Check whether the user exists
    GET usernames/(?P<username>\w{5,20})/
    1、创建一个类视图
    2、校验参数
    3、查询数据
    4、返回校验的结果
    """

    # 2、校验参数
    def get(self,request,username):

        count = Users.objects.filter(username=username).count()
        # if not count:
        #     return HttpResponse("可以注册")
        # else:
        #     return HttpResponse("不能注册")
        # data = {
        #     "username": username,
        #     "status": count,
        #     "message": "可以注册" if not count else "已被注册",
        # }

        # 3、查询数据

        data = {
            'username': username,
            'count':count
        }


        # 4、返回校验的结果
        return to_json_data(data=data)
        # return JsonResponse(data=data)





