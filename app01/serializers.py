from .models import *
from rest_framework import serializers


# serializer 类需要继承 serializers.Serializer，
# 然后实现父类的 update，create 方法
class UserInfoSerializer(serializers.Serializer):
    # 声明需要被序列化和反序列化的字段，同 model 的字段，
    # 字段名注意需要同 model 字段同名
    id = serializers.IntegerField(read_only=True, label='id')
    name = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)
    phone = serializers.CharField(max_length=64)
    status = serializers.BooleanField()
    create_time = serializers.DateTimeField()
    last_login = serializers.DateTimeField()


    # 定义创建方法
    def create(self, validated_date):
        return UserInfo.objects.all()

    # 定义修改方法
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.modified_time = validated_data.get('modified_time', instance.modified_time)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)

class PortSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True, label='id')
    name = serializers.CharField(max_length=64)
    nowCity = serializers.CharField(max_length=64)

class ShipTypeSerializer(serializers.Serializer):
    # 声明需要被序列化和反序列化的字段，同 model 的字段，
    # 字段名注意需要同 model 字段同名
    id = serializers.IntegerField(read_only=True, label='id')
    name = serializers.CharField(max_length=64)


class ShipInfoSerializer(serializers.Serializer):
        # 声明需要被序列化和反序列化的字段，同 model 的字段，
        # 字段名注意需要同 model 字段同名
        id = serializers.IntegerField(read_only=True, label='id')
        name = serializers.CharField(max_length=64)
        # type = serializers.PrimaryKeyRelatedField(many=False, queryset=ShipType.objects.all())
        speed = serializers.IntegerField()
        # port = serializers.PrimaryKeyRelatedField(many=False, queryset=Port.objects.all())
        type = serializers.SerializerMethodField()
        port = serializers.SerializerMethodField()
        capacity = serializers.IntegerField()
        price = serializers.IntegerField()

        def get_type(self, obj):
            return obj.type.typeName
        def get_port(self, obj):
            return obj.port.name

        def create(self, validated_date):
            return ShipInfo.objects.all()


class CargoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, label='id')
    name = serializers.CharField(max_length=64)
    type = serializers.CharField(max_length=64)
    weight = serializers.IntegerField()
    user = serializers.SerializerMethodField()
    status = serializers.BooleanField()
    def get_user(self, obj):
        return obj.user.name

class OrderSerializer(serializers.Serializer):

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
    id = serializers.IntegerField(read_only=True, label='id')
    orderNum = serializers.CharField()
    ship =  serializers.SerializerMethodField()
    cargo =  serializers.SerializerMethodField()

    price = serializers.IntegerField()

    status = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField()

    start_port = serializers.SerializerMethodField()
    end_port = serializers.SerializerMethodField()
    distance = serializers.IntegerField()

    is_commented = serializers.BooleanField()
    comment = serializers.SerializerMethodField()

    Remark = serializers.CharField()
    user = serializers.SerializerMethodField()
    kuaidiNum = serializers.CharField()

    def get_user(self, obj):
        return obj.user.name
    def get_ship(self, obj):
        print(obj)
        return obj.ship.name
    def get_cargo(self, obj):
        return obj.cargo.name
    def get_start_port(self, obj):
        return obj.start_port.name
    def get_end_port(self, obj):
        return obj.end_port.name

    def get_status(self, obj):
        return obj.get_status_display()
    def get_comment(self, obj):
        return obj.get_comment_display()

