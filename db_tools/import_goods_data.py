# _*_ coding: utf-8 _*_
#Author: Scott.Yu
# @Time     : 2019/6/27 20:51
# @Author   : Scott.Yu
# @Email    : gitwork_scott@sina.com
# @File     : import_goods_data.py
# @SoftWare : ContractMS

#独立使用django的model

import sys, os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ContractMS.settings')

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name) # 使用filter而不用get是为了避免取不到数据或者取到两条数据的时候会出现报错的情况

    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()