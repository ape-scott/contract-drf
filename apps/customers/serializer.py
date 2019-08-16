# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice
from rest_framework import serializers
from django.contrib.auth import get_user_model

from customers.models import Customers, CustomerUsers, CustomerBillInfo
from users.serializer import UserListSerializer

User = get_user_model()


class CustomersDetailSerializer(serializers.ModelSerializer):
    """
    客户详情序列化类
    """
    customer_type = serializers.ChoiceField(choices=Customers.CATEGORY_TYPE, default=99)
    customer_level = serializers.ChoiceField(choices=Customers.LEVEL_TYPE, default=6)

    class Meta:
        model = Customers
        fields = "__all__"

class CustomerUsersSerializer(serializers.ModelSerializer):
    '''
    客户联系人
    '''
    # customer = CustomersDetailSerializer()
    # user = UserDetailSerializer()
    class Meta:
        model = CustomerUsers
        fields = "__all__"

class CustomerBillInfoSerializer(serializers.ModelSerializer):
    '''
    客户联系人
    '''
    customer = CustomersDetailSerializer()
    user = UserListSerializer()
    class Meta:
        model = CustomerBillInfo
        fields = "__all__"
