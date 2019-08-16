from django.db import models

# Create your models here.

from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

from django.contrib.auth import get_user_model
User = get_user_model()

from utils.tools import createFileNo

from customers.models import Customers

class Contracts(models.Model):
    '''
    合同信息表
    '''
    CRT_TYPE = (
        (1, "软件开发"),
        (2, "销售代理"),
        (3, "自有产品"),
        (4, "系统集成"),
        (5, "人员外包"),
        (6, "维护合同")
    )
    CRT_PROSTATE = (
        ("00", "未开始"),
        ("01", "执行中"),
        ("02", "执行完毕"),
        ("03", "已取消"),
    )
    CRT_SIGNEDSTATE = (
        ("00", "未签订"),
        ("01", "签订中"),
        ("02", "已签订"),
        ("03", "已取消"),
    )
    crt_name = models.CharField(max_length=100, verbose_name="合同名称")
    crt_fileno = models.CharField(max_length=20, default=createFileNo, unique=True, verbose_name="合同档案号")
    crt_serialnumber = models.CharField(max_length=20, null=True, blank=True, verbose_name="合同编号")
    crt_type = models.IntegerField(choices=CRT_TYPE, verbose_name="合同分类", help_text="合同分类")
    crt_customer = models.ForeignKey(Customers, related_name="contract_customer",verbose_name="客户公司名称",
                                     on_delete=models.DO_NOTHING)
    crt_amt = models.DecimalField( max_digits=11, decimal_places=2, verbose_name="合同金额")
    crt_currency = models.CharField(max_length=3, default='CNY', verbose_name="币种名称")
    crt_salesrep = models.CharField(max_length=20, null=True, blank=True, verbose_name="销售代表")
    crt_salesarea = models.CharField(max_length=20, null=True, blank=True, verbose_name="销售区域")
    crt_signeddate = models.DateField(null=True, blank=True, verbose_name="签订日期")
    crt_registerdate = models.DateField(auto_now_add=True, verbose_name="登记日期")
    crt_prostate = models.CharField(max_length=2, choices=CRT_PROSTATE, default='00', verbose_name="执行状态")
    crt_signedstate = models.CharField(max_length=2, choices=CRT_SIGNEDSTATE, default='00', verbose_name="签订状态")
    crt_effectivedate = models.DateField(null=True, blank=True, verbose_name="合同有效起始日期")
    crt_enddate = models.DateField(null=True, blank=True, verbose_name="合同结束日期")
    crt_desc = UEditorField(verbose_name=u"合同备注", null=True, blank=True, imagePath="contract/images/", width=1000,
                                 height=300, filePath="contract/files/", default='')
    crt_createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    crt_updatetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '合同信息'
        verbose_name_plural = verbose_name

    # def _do_insert(self, manager, using, fields, update_pk, raw):
    #     """
    #     Do an INSERT. If update_pk is defined then this method should return
    #     the new pk for the model.
    #     """
    #     self.crt_desc = '123123123sdsfsd'
    #     return manager._insert([self], fields=fields, return_id=update_pk,
    #                            using=using, raw=raw)
    def __str__(self):
        return str(self.crt_name) if self.crt_name else ''
