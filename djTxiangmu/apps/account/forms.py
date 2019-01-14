from django import forms
from apps.forms import FormMixin


# 表单验证
class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"min_length": "手机号长度有误", "max_length": "手机号长度有误", "required": "手机号不能为空"})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度有误", "max_length": "密码长度有误", "required": "密码不能为空"})
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form,FormMixin):
    pass
