# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice

"""contractservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from contractservice.settings import MEDIA_ROOT
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.autodiscover()
# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

#路由注册配置
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, OrganizationViewSet, MenuViewSet, PermissionViewSet, RoleViewSet
from customers.views import CustomersViewSet, CustomersUsersViewSet
from contracts.views import ContractsViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, base_name="users")
router.register(r'organizations', OrganizationViewSet, base_name="organization")
router.register(r'menus', MenuViewSet, base_name="menus")
router.register(r'permissions', PermissionViewSet, base_name="permissions")
router.register(r'roles', RoleViewSet, base_name="roles")
router.register(r'customers', CustomersViewSet, base_name="customers")
router.register(r'customers_user', CustomersUsersViewSet, base_name="customersusers")
router.register(r'contracts', ContractsViewSet, base_name="contracts")
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    #jwt认证模式
    url(r'^login/', obtain_jwt_token),

    url(r'^', include(router.urls)),

    #rest_framework docs
    url(r'docs/', include_docs_urls(title="合同管理系统"))
]
