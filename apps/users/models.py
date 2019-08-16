# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    path = models.CharField(max_length=158, null=True, blank=True, verbose_name="链接地址")
    is_frame = models.BooleanField(default=False, verbose_name="外部菜单")
    is_show = models.BooleanField(default=True, verbose_name="显示标记")
    sort = models.IntegerField(null=True, blank=True, verbose_name="排序标记")
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name="组件")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']

class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="权限名")
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父权限")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']

class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门")
    )
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=organization_type_choices, default="company", verbose_name="类型")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类组织")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UsersProfile(AbstractUser):
    '''
    用户
    '''
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    user_image = models.ImageField(upload_to="users/images/%Y%m/", default="image/default.png",null=True, blank=True, verbose_name="头像")
    department = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True, default="guest")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.name) if self.name else self.username
        # return  self.username
