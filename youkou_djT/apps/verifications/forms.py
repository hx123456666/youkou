import re

from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from apps.users.models import Users

# 创建手机号的正则校验器
mobile_validator = RegexValidator(r"^1[3-9]\d{9}$", "手机号码格式不正确")


class CheckImgCodeForm(forms.Form):
    """
    check sms code
    """
    mobile = forms.CharField(max_length=11, min_length=11, validators=[mobile_validator, ],
                             error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})
    image_code_id = forms.UUIDField(error_messages={"required": "图片UUID不能为空"})
    text = forms.CharField(max_length=4, min_length=4,
                           error_messages={"min_length": "图片验证码长度有误", "max_length": "图片验证码长度有误",
                                           "required": "图片验证码不能为空"})

    # Cleaning and validating fields that depend on each other
    # import re

    # 这种方式只能做一项数据的校验
    # def clean_mobile(self):
    #     """
    #
    #     :return:
    #
    #     """
    #     tel = self.cleaned_data.get('mobile')
    #     if not re.match(r"^1[3-9]\d{9}$",tel):
    #         raise forms.ValidationError("手机号码格式不正确")
    #
    #     if Users.objects.filter(mobile=tel).exists():
    #         raise forms.ValidationError("手机号已注册，请重新输入")

    def clean(self):
        cleaned_data = super().clean()


        image_uuid = cleaned_data.get('image_code_id')
        image_text = cleaned_data.get('text')
        mobile_num = cleaned_data.get('mobile')

        if not re.match(r"^1[3-9]\d{9}$",mobile_num):
            raise forms.ValidationError("手机号码格式不正确")

        if Users.objects.filter(mobile=mobile_num).count():
            raise forms.ValidationError("手机号已注册，请重新输入")

        # 1、获取图片验证码
        con_redis = get_redis_connection(alias='verify_codes')
        img_key = "img_{}".format(image_uuid).encode("utf-8")
        real_image_code = con_redis.get(img_key)

        # 2、判断用户输入的图片验证码是否正确
        if(not real_image_code) or (not image_text != real_image_code):
            raise forms.ValidationError("图片验证失败")

        # 3、判断在60s内是否有发送过短信的记录
        sms_flag_fmt = "sms_flag_{}".format(mobile_num).encode("utf-8")
        sms_flag = con_redis.get(sms_flag_fmt)

        if sms_flag:
            raise forms.ValidationError("获取手机短信验证码过于频繁")









    # def clean(self):
    #     cleaned_data = super().clean()
    #     # 1、
    #     image_uuid = cleaned_data.get("image_code_id")
    #     image_text = cleaned_data.get("text")
    #     mobile_num = cleaned_data.get("mobile")
    #
    #     # 2、
    #     if Users.objects.filter(mobile=mobile_num).count():
    #         raise forms.ValidationError("手机号已注册，请重新输入")
    #
    #     # 确保settings.py文件中有配置redis CACHE
    #     # Redis原生指令参考 http://redisdoc.com/index.html
    #     # Redis python客户端 方法参考 http://redis-py.readthedocs.io/en/latest/#indices-and-tables
    #     # 2、
    #     con_redis = get_redis_connection(alias='verify_codes')
    #     # 创建保存到redis中图片验证码的key
    #     img_key = "img_{}".format(image_uuid).encode('utf-8')
    #
    #     # 取出图片验证码
    #     real_image_code_origin = con_redis.get(img_key)
    #     real_image_code = real_image_code_origin.decode('utf-8') if real_image_code_origin else None
    #     con_redis.delete(img_key)
    #
    #     # 验证手机号
    #     if (not real_image_code) or (image_text != real_image_code):
    #         raise forms.ValidationError("图片验证失败")
    #
    #     # 检查是否在60s内有发送记录
    #     sms_flag_fmt = "sms_flag_{}".format(mobile_num).encode('utf-8')
    #     sms_flag = con_redis.get(sms_flag_fmt)
    #     if sms_flag:
    #         raise forms.ValidationError("获取手机短信验证码过于频繁")
