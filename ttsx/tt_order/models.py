from django.db import models
from tt_goods.models import *

# Create your models here.

#coding=utf-8


class OrderInfo(models.Model):
    oid=models.CharField(max_length=20, primary_key=True)
    user=models.ForeignKey('tt_user.UserInfo')
    odate=models.DateTimeField(auto_now_add=True)
    oIsPay=models.BooleanField(default=False)
    ototal=models.DecimalField(max_digits=6,decimal_places=2)
    oaddress=models.CharField(max_length=150)


class OrderDetailInfo(models.Model):
    goods=models.ForeignKey(GoodsInfo)
    order=models.ForeignKey(OrderInfo)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    count=models.IntegerField()