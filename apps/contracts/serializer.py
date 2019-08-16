# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice
from rest_framework import serializers
from django.contrib.auth import get_user_model

from customers.models import Customers, CustomerUsers
from users.serializer import UserListSerializer
from contracts.models import Contracts
from customers.serializer import CustomersDetailSerializer

User = get_user_model()


class ContractsDetailSerializer(serializers.ModelSerializer):
    """
    合同信息序列化类
    """
    # crt_customer = CustomersDetailSerializer(read_only=True)
    def to_representation(self, instance):
        self.fields['crt_customer'] = CustomersDetailSerializer(read_only=True)
        return super().to_representation(instance)

    # def validate_crt_fileno(self, crt_fileno):
    #     if(self.action = 'create'):
    #         if Contracts.objects.filter(crt_fileno=crt_fileno):
    #             raise serializers.ValidationError('该合同已经存在，合同档案号：'+ crt_fileno)
    #     return crt_fileno

    class Meta:
        model = Contracts
        fields = "__all__"
