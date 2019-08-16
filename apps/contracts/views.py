from django.shortcuts import render

# Create your views here.

# 引入drf的类
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

##引入jwt认证控制类
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from django_filters.rest_framework import DjangoFilterBackend

# 引入app的类
from .models import Contracts
from .serializer import ContractsDetailSerializer

class ContractsViewSet(viewsets.ModelViewSet):
    """
    合同信息的查询，创建，更新，删除，过滤，搜索，排序
    """
    ## 权限控制
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    queryset = Contracts.objects.all()
    serializer_class = ContractsDetailSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('crt_createtime', 'crt_updatetime', 'crt_customer', 'crt_name', 'crt_fileno', 'crt_serialnumber',
                     'crt_type')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
