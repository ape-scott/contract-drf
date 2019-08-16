# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/7/10 11:05
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : serializer.py
# @SoftWare : contractservice

from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class TimeAbstract(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True

class Customers(TimeAbstract):
    """
    客户信息表
    """
    CATEGORY_TYPE = (
        (1, "管理性银行"),
        (2, "政策性银行"),
        (3, "股份制商业银行"),
        (4, "外资银行"),
        (5, "城市商业银行"),
        (6, "城市信用社"),
        (7, "农联社"),
        (8, "村镇银行"),
        (9, "金融监管机构"),
        (10, "政府"),
        (11, "企业"),
        (12, "保险"),
        (13, "证券"),
        (14, "合作伙伴"),
        (15, "竞争对手"),
        (99, "其他"),
    )
    LEVEL_TYPE = (
        (1, "VIP客户"),
        (2, "战略客户"),
        (3, "潜力客户"),
        (4, "核心客户"),
        (5, "重要客户"),
        (6, "一般客户"),
        (7, "合作伙伴"),
    )
    STATE = (
        ("00", "新增待审核"),
        ("01", "修改待审核"),
        ("02", "删除待审核"),
        ("10", "正常"),
        ("20", "已删除"),
    )
    customer_name = models.CharField(max_length=100, verbose_name="客户公司名称")
    customer_sh_name = models.CharField(max_length=20,null=True, blank=True, verbose_name="客户公司简称")
    customer_old_name = models.CharField(max_length=100,null=True, blank=True, verbose_name="客户公司曾用名")
    customer_addr = models.CharField(max_length=200,null=True, blank=True, verbose_name="客户公司地址")
    customer_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="客户类别", help_text="客户类别")
    customer_level = models.IntegerField(choices=LEVEL_TYPE, verbose_name="客户级别", help_text="客户级别")
    customer_desc = UEditorField(verbose_name=u"客户备注", null=True, blank=True, imagePath="customer/images/", width=1000,
                                 height=300, filePath="customer/files/", default='')
    customer_stat = models.CharField(choices=STATE, max_length=2, default='00', verbose_name="客户状态")

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return str(self.customer_name) if self.customer_name else ''

class CustomerUsers(TimeAbstract):
    '''
    客户联系人
    '''
    name = models.CharField(max_length=50, verbose_name="联系人名称")
    jobtitle = models.CharField(max_length=100, null=True, blank=True,verbose_name="联系人职位")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="联系人手机")
    telephone = models.CharField(null=True, blank=True, max_length=20, verbose_name="联系人电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="联系人邮箱")
    fax = models.CharField(null=True, blank=True, max_length=20, verbose_name="联系人传真")
    customer= models.ForeignKey(Customers, verbose_name="客户公司名称", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '客户联系人'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return "%s(%s)".format(self.name, self.mobile)

class CustomerBillInfo(TimeAbstract):
    '''
    客户开票信息
    :param TimeAbstract:
    :return:
    '''
    customer= models.ForeignKey(Customers, verbose_name="客户公司名称", on_delete=models.DO_NOTHING)
    taxes_num = models.CharField(max_length=50, verbose_name="纳税识别号")
    account = models.CharField(max_length=30, null=True, blank=True, verbose_name="账号")
    account_name = models.CharField(max_length=60, null=True, blank=True, verbose_name="户名")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="地址")
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name="电话")
    user = models.ForeignKey(User, verbose_name="创建用户", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '开票信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)".format(self.customer, self.taxes_num)
