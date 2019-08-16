# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice

from django.shortcuts import render

# Create your views here.

from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework import mixins
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication

from django_filters.rest_framework import DjangoFilterBackend


from .models import Customers, CustomerUsers
from .serializer import CustomersDetailSerializer, CustomerUsersSerializer
from .filters import CustomersUsersFilter

class CustomersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class CustomersViewSet(viewsets.ModelViewSet):
    """
    客户信息的查询，过滤，搜索，排序
    """
    ## 权限控制
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    queryset = Customers.objects.all()
    serializer_class = CustomersDetailSerializer
    # pagination_class = CustomersPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ('customer_name','customer_level','customer_type','customer_stat',)
    search_fields = ('customer_name', 'customer_desc')
    ordering_fields = ('customer_name', 'customer_level')

    def create(self, request, *args, **kwargs):
        # print(request.data['customer_old_name'])
        # request.data['customer_old_name']='123123123123'
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()



class CustomersUsersViewSet(viewsets.ModelViewSet):
    """
    客户信息的查询，过滤，搜索，排序
    """
    ## 权限控制
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    queryset = CustomerUsers.objects.all()
    serializer_class = CustomerUsersSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = CustomersUsersFilter

class CustomersBillInfoViewSet(viewsets.ModelViewSet):
    """
    客户信息的查询，过滤，搜索，排序
    """
    ## 权限控制
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    queryset = CustomerUsers.objects.all()
    serializer_class = CustomerUsersSerializer
    filter_backends = (DjangoFilterBackend, )

