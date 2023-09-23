from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
import datetime
class Admin(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        verbose_name = "用户列表"

class ShipType(models.Model):
    typeName = models.CharField(max_length=64)

class Port(models.Model):
    name = models.CharField(max_length=64)
    nowCity = models.CharField(max_length=64)

class ShipInfo(models.Model):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(ShipType,on_delete=models.CASCADE)
    port =  models.ForeignKey(Port,on_delete=models.CASCADE)
    speed = models.IntegerField(default=50)

    capacity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        verbose_name = "船舶列表"

class Cargo(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    weight = models.IntegerField()
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )

    ship =  models.ForeignKey(ShipInfo,on_delete=models.CASCADE)
    cargo =  models.ForeignKey(Cargo,on_delete=models.CASCADE)

    price = models.IntegerField()

    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")
    create_time = models.DateTimeField(auto_now_add=True)

    start_port = models.ForeignKey(Port,on_delete=models.CASCADE, related_name='start_port')
    end_port = models.ForeignKey(Port,on_delete=models.CASCADE, related_name='end_port')
    distance = models.IntegerField()

    is_commented = models.BooleanField(default=False, verbose_name='是否评价了')
    comment = models.SmallIntegerField(choices=SCORE_CHOICES, default=1, verbose_name="订单状态")

    Remark = models.TextField()
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    orderNum = models.CharField(max_length=50)
    kuaidiNum = models.CharField(max_length=50,default="")


