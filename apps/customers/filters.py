# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/6/29 10:50
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : filters.py
# @SoftWare : ContractMS

import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Customers, CustomerUsers


class CustomersUsersFilter(filters.FilterSet):
    customer = filters.NumberFilter(field_name='customer',)
    class Meta:
        model = CustomerUsers
        fields = [ 'customer', 'id']
