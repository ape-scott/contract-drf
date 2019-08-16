# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

from .models import Role, Permission, Menu, Organization


User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = User
        fields = ['id', 'name', 'gender', 'birthday', 'email', 'mobile', 'user_image', 'department', 'position',
                  'superior','is_active', 'roles']
        depth = 1

class UserModifySerializer(serializers.ModelSerializer):
    '''
    用户编辑的序列化
    '''
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['id', 'name', 'gender', 'birthday', 'email', 'mobile', 'user_image', 'department', 'position',
                  'superior', 'is_active', 'roles']

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    # username = serializers.CharField(required=True, allow_blank=False)
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['id', 'name', 'gender', 'birthday', 'email', 'mobile', 'department', 'position',
                  'superior', 'is_active', 'roles', 'password']

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile


class RoleListSerializer(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    class Meta:
        model = Role
        fields = '__all__'

class RoleModifySerializer(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    class Meta:
        model = Role
        fields = '__all__'

class PermissionListSerializer(serializers.ModelSerializer):
    '''
    权限列表序列化
    '''
    menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id','name','method','menuname','pid')


class OrganizationSerializer(serializers.ModelSerializer):
    '''
    组织架构序列化
    '''
    type = serializers.ChoiceField(choices=Organization.organization_type_choices, default='company')

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')


class OrganizationUserTreeSerializer(serializers.ModelSerializer):
    '''
    组织架构树序列化
    '''
    label = serializers.StringRelatedField(source='name')
    children = UserSerializer(many=True, read_only=True, source='userprofile_set')

    class Meta:
        model = Organization
        fields = ('id', 'label', 'pid', 'children')


class MenuSerializer(serializers.ModelSerializer):
    '''
    菜单序列化
    '''

    class Meta:
        model = Menu
        fields = ('id', 'name', 'icon', 'path', 'is_show','is_frame', 'sort', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}
