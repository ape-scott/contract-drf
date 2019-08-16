# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/8/12 15:25
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : signals.py
# @SoftWare : contractservice

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Contracts


@receiver(post_save, sender=Contracts)
def create_Contract(sender, instance=None, created=False, **kwargs):
    if created:
        instance.crt_desc = '12312322222kdkdkd'
        instance.save()
