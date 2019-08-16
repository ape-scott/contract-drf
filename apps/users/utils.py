# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/9 22:48
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : utils.py
# @SoftWare : ContractMS

from .serializer import UserListSerializer
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
        'access': ['admin'],
        'user': UserListSerializer(user, context={'request': request}).data
    }
