# 第一部分导入的是Python（系统的）的模块
import json
import logging
import string
import random




# 第二部分导入的是Django内的模块
# from django.shortcuts import render,redirect,reverse


from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse, JsonResponse

# 第三部分导入的是我们自己写的模块
from utils.captcha.captcha import captcha
from utils.res_code import Code, error_map
from utils.yuntongxun.sms import CCP
from . import constants
from apps.verifications import forms
from apps.users.models import Users
from utils.json_fun import to_json_data


# 导入日记器
logger = logging.getLogger('django')

# 图片验证码的实现
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


# 判断用户名是否能创建的实现
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



# 判断手机是否注册功能实现

class CheckMobilesView(View):
    """
        Check whether the mobiles exists
        GET mobiles/(?P<mobiles>\w{11})/
        1、创建一个类视图
        2、校验参数
        3、查询数据
        4、返回校验结果
        """
    def get(self,request,mobile):

        count = Users.objects.filter(mobile=mobile).count()

        data = {
            "mobile":mobile,
            "count":count
        }
        return to_json_data(data=data)



# 1、创建一个类视图
class SmsCodesView(View):
    """
    send mobile sms code
    POST /sms_codes/
    1、创建一个类视图
    2、获取前端参数
    3、校验参数
    4、发生短信验证码
    5、保存短信验证码到redis
    6、返回前端
    """

    def post(self,request):
        # 2、获取前端参数
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data)
        # 3、校验参数
        # mobile = dict_data.get('mobile')
        form = forms.CheckImgCodeForm(data=dict_data) # 定义一个表单对象
        if form.is_valid():
            # 4、发生短信验证码
            mobile = form.cleaned_data.get('mobile') # 获取手机号
            sms_num =''.join([random.choice(string.digits) for _ in range(constants.SMS_CODE_NUMS)]) # 创建短信验证码内容

            # 5、保存短信验证码到redis
            # 确保settings.py文件中有配置redis CACHE
            # Redis原生指令参考 http://redisdoc.com/index.html
            # Redis python客户端 方法参考 http://redis-py.readthedocs.io/en/latest/#indices-and-tables
            redis_con = get_redis_connection(alias="verify_codes")


            sms_flag_fmt = "sms_flag_{}".format(mobile).encode("utf-8") # 构造短信验证码的key,即短信验证码的记录
            sms_text_fmt = "sms_{}".format(mobile).encode("utf-8") # 构造短信验证码的文本

            # redis_con.setex(sms_flag_fmt,constants.SEND_SMS_CODE_INTERVAL,sms_text_fmt)
            p1 = redis_con.pipeline()  # 定义一个管道
            # 此处设置为True会出现bug
            try:
                p1.setex(sms_flag_fmt,constants.SEND_SMS_CODE_INTERVAL,1)
                p1.setex(sms_text_fmt,constants.SMS_CODE_REDIS_EXPIRES,sms_num)
                # 让管道通知redis执行命令
                p1.execute()
            except Exception as e:
                logger.debug("redis 执行出现异常：{}".format(e))
                return to_json_data(errno=Code.UNKOWNERR,errmsg=error_map[Code.UNKOWNERR])
            logger.info("Sms Code: {}".format(sms_num))

            # 测试时短信验证码发送代码,把发送短信验证码先注释掉
    # def set_sms(self,mobile,sms_num):
            logger.info("发送验证码电信[正常][ moblie : %s sms_code: %s]" % (mobile,sms_num))
            return to_json_data(errno=Code.OK,errmsg="短信验证码发送成功！")



            # # 发送短语验证码
            # try:
            #     result = CCP().send_template_sms(mobile,
            #                                      [sms_num, constants.SMS_CODE_REDIS_EXPIRES],
            #                                      constants.SMS_CODE_TEMP_ID)
            # except Exception as e:
            #     logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
            #     return to_json_data(errno=Code.SMSERROR, errmsg=error_map[Code.SMSERROR])
            # else:
            #     if result == 0:
            #         logger.info("发送验证码短信[正常][ mobile: %s sms_code: %s]" % (mobile, sms_num))
            #         return to_json_data(errno=Code.OK, errmsg="短信验证码发送成功")
            #     else:
            #         logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
            #         return to_json_data(errno=Code.SMSFAIL, errmsg=error_map[Code.SMSFAIL])

        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
                # print(item[0].get('message'))   # for test
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)


        # 6、返回前端




