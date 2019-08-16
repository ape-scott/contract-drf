# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/8/12 10:50
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : tools.py
# @SoftWare : contractservice

from datetime import datetime
import random

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.basic import ConResponse
from rest_framework.generics import ListAPIView

class TreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)

class TreeAPIView(ListAPIView):
    '''
    自定义树结构View
    '''
    serializer_class = TreeSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return ConResponse(results)

class CommonPagination(PageNumberPagination):
    '''
    分页设置
    '''
    page_size = 10
    page_size_query_param = 'size'


class ConPermission(BasePermission):
    '''
    自定义权限
    '''

    @classmethod
    def get_permission_from_role(self, request):
        try:
            perms = request.user.roles.values(
                'permissions__method',
            ).distinct()
            return [p['permissions__method'] for p in perms]
        except AttributeError:
            return None

    def has_permission(self, request, view):
        perms = self.get_permission_from_role(request)
        if perms:
            if 'admin' in perms:
                return True
            elif not hasattr(view, 'perms_map'):
                return True
            else:
                perms_map = view.perms_map
                _method = request._request.method.lower()
                for i in perms_map:
                    for method, alias in i.items():
                        if (_method == method or method == '*') and alias in perms:
                            return True

def createFileNo():
    return datetime.now().strftime("%Y%m%d%H%M")+ ''.join(random.sample('0123456789ABCDEFGHJKLMNPQRSTUVWXYX', 8))

