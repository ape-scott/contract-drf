# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from operator import itemgetter
from django.contrib.auth.hashers import check_password


from apps.utils.tools import TreeAPIView, CommonPagination, ConPermission, ConResponse
from apps.utils.code import *

from .models import Menu, Role, Organization, Permission

from .serializer import MenuSerializer, OrganizationSerializer, OrganizationUserTreeSerializer
from .serializer import PermissionListSerializer, RoleListSerializer, RoleModifySerializer
from .serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user:
                if user.check_password(password):
                    return user
            return None
        except Exception as e:
            return None

class UserViewset_bak(viewsets.ModelViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def get_serializer_class(self):
        return UserListSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class MenuViewSet(viewsets.ModelViewSet, TreeAPIView):
    '''
    菜单管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'menu_all'}, {'get': 'menu_list'}, {'post': 'menu_create'}, {'put': 'menu_edit'},
                 {'delete': 'menu_delete'})
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('sort',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (ConPermission,)



class MenuTreeView(TreeAPIView):
    '''
    菜单树
    '''
    queryset = Menu.objects.all()



class OrganizationViewSet(viewsets.ModelViewSet, TreeAPIView):
    '''
    组织机构：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'organization_all'}, {'get': 'organization_list'}, {'post': 'organization_create'},
    {'put': 'organization_edit'},{'delete': 'organization_delete'})
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (ConPermission,)


class OrganizationTreeView(TreeAPIView):
    '''
    组织架构树
    '''
    queryset = Organization.objects.all()


class OrganizationUserTreeView(APIView):
    '''
    组织架构关联用户树
    '''
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        organizations = Organization.objects.all()
        serializer = OrganizationUserTreeSerializer(organizations, many=True)
        tree_dict = {}
        tree_data = []
        for item in serializer.data:
            new_item = {
                'id': 'o' + str(item['id']),
                'label': item['label'],
                'pid': item['pid'],
                'children': item['children']
            }
            tree_dict[item['id']] = new_item
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent['children'].append(tree_dict[i])
            else:
                tree_data.append(tree_dict[i])
        return ConResponse(tree_data)



class PermissionViewSet(viewsets.ModelViewSet, TreeAPIView):
    '''
    权限：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'permission_all'}, {'get': 'permission_list'}, {'post': 'permission_create'},
                 {'put': 'permission_edit'},{'delete': 'permission_delete'})
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (ConPermission,)


class PermissionTreeView(TreeAPIView):
    '''
    权限树
    '''
    queryset = Permission.objects.all()


class RoleViewSet(viewsets.ModelViewSet):
    '''
    角色管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'role_all'}, {'get': 'role_list'}, {'post': 'role_create'}, {'put': 'role_edit'},
                 {'delete': 'role_delete'})
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (ConPermission,)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleModifySerializer


class UserInfoView(APIView):
    '''
    获取当前用户信息和权限
    '''
    @classmethod
    def get_permission_from_role(self, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None

    def get(self, request):
        if request.user.id is not None:
            perms = self.get_permission_from_role(request)
            data = {
                'id': request.user.id,
                'username': request.user.username,
                'avatar': request._request._current_scheme_host + '/media/' + str(request.user.image),
                'email': request.user.email,
                'is_active': request.user.is_active,
                'createTime':request.user.date_joined,
                'roles': perms
            }
            return ConResponse(data, status=OK)
        else:
            return ConResponse('请登录后访问!', status=FORBIDDEN)

class UserBuildMenuView(APIView):
    '''
    绑定当前用户菜单信息
    '''
    def get_menu_from_role(self, request):
        if request.user:
            menu_dict = {}
            menus = request.user.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__pid'] is None:
                    if item['menus__is_frame']:
                        # 判断是否外部链接
                        top_menu = {
                            'id': item['menus__id'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'children': [{
                                'path': item['menus__path'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                }
                            }],
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        top_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': '/' + item['menus__path'],
                            'redirect': 'noredirect',
                            'component': 'Layout',
                            'alwaysShow': True,
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon']
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'children': []
                        }
                    menu_dict[item['menus__id']] = top_menu
                else:
                    if item['menus__is_frame']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    elif item['menus__is_show']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'noCache': True,
                            },
                            'hidden': True,
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        '''
        获取所有菜单数据，重组结构
        '''
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                if item['is_frame']:
                    # 判断是否外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'Layout',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'redirect': 'noredirect',
                        'component': 'Layout',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'Layout',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict

    def get_all_menus(self, request):
        perms = UserInfoView.get_permission_from_role(request)
        tree_data = []
        if 'admin' in perms or request.user.is_superuser:
            tree_dict = self.get_all_menu_dict()
        else:
            tree_dict = self.get_menu_from_role(request)
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent.setdefault('redirect', 'noredirect')
                parent.setdefault('alwaysShow', True)
                parent.setdefault('children', []).append(tree_dict[i])
                parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
            else:
                tree_data.append(tree_dict[i])
        return tree_data

    def get(self, request):
        if request.user.id is not None:
            menu_data = self.get_all_menus(request)
            return ConResponse(menu_data, status=OK)
        else:
            return ConResponse('请登录后访问!',status=FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    '''
    用户管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    permission_classes = (ConPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        request.data['password'] = '123456'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return ConResponse(serializer.data, status=CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # 删除用户时删除其他表关联的用户
        instance = self.get_object()
        id = str(kwargs['pk'])
        # projects = Project.objects.filter(
        #     Q(user_id__icontains=id + ',') | Q(user_id__in=id) | Q(user_id__endswith=',' + id)).values()
        # if projects:
        #     for project in projects:
        #         user_id = project['user_id'].split(',')
        #         user_id.remove(id)
        #         user_id = ','.join(user_id)
        #         Project.objects.filter(id=project['id']).update(user_id=user_id)
        # ConnectionInfo.objects.filter(uid_id=id).delete()
        self.perform_destroy(instance)
        return ConResponse(status=NO_CONTENT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='change-passwd', url_name='change-passwd')
    def set_password(self, request, pk=None):
        perms = UserInfoView.get_permission_from_role(request)
        user = User.objects.get(id=pk)
        if 'admin' in perms or 'user_all' in perms or request.user.is_superuser:
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return ConResponse('密码修改成功!')
            else:
                return ConResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
        else:
            old_password = request.data['old_password']
            if check_password(old_password, user.password):
                new_password1 = request.data['new_password1']
                new_password2 = request.data['new_password2']
                if new_password1 == new_password2:
                    user.set_password(new_password2)
                    user.save()
                    return ConResponse('密码修改成功!')
                else:
                    return ConResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
            else:
                return ConResponse('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)
