from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as _UserManager

# Create your models here.

class UserManager(_UserManager):

    """
    define user manager for modifing 'no need email'
    when 'python manager.py createsuperuser '
    """

    def create_superuser(self,username,password,email=None,**extra_fields):

        super(UserManager,self).create_superuser(username=username,password=password,email=email,**extra_fields)

class Users(AbstractUser):

    """
    add moble、email_active fileds to Django users models.
    """

    objects = UserManager()

    # A list of the field names that will be prompted for
    # when creating a user via the createsuperuser management command.

    REQUIRED_FIELDS = ['mobile']

    mobile = models.CharField(max_length=11,unique=True,verbose_name="手机号码",help_text="手机号码", error_messages={'unique':'此手机号已经注册'}
                              )
    email_active = models.BooleanField(default=False,verbose_name="邮箱验证状态")

    class Meta:
        db_table = 'tb_users'  # 指明数据库表名字
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name # 显示复数名称


    def __str__(self):
        return self.username









