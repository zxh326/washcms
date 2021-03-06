import time
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.
# class UserProfile


class User(models.Model):

    class Meta:
        verbose_name = "所有用户"
        verbose_name_plural = "Users"
        ordering = ['-last_login']

    type_level = (
        (0, u'管理员'),
        (1, u'库管'),
        (2, u'配送员'),
        (3, u'顾客'),
        (4, u'未注册')
    )
    wk = models.CharField(
        max_length=100,
        null=False,
        primary_key=True
    )
    user_type = models.IntegerField(
        default=4,
        choices=type_level,
        verbose_name='用户身份'
    )
    nick_name = models.CharField(
        max_length=100,
        default='nick_name'
    )
    avatar_links = models.CharField(
        max_length=150,
        default='https://pic3.zhimg.com/aadd7b895_s.jpg'
    )
    reg_date = models.DateTimeField(
        auto_now_add=True
    )
    last_login = models.DateTimeField(default=timezone.now)

    @staticmethod
    def all_admin():
        return User.objects.all().filter(user_type=0)

    @staticmethod
    def all_courier():
        return User.objects.all().filter(user_type=2)

    @staticmethod
    def all_customer():
        return User.objects.all().filter(user_type=3)

    @staticmethod
    def user_all():
        return User.objects.all()

    def __len__(self):
        return len(User.user_all())

    def __str__(self):
        return self.nick_name


class DeliveryArea(models.Model):

    class Meta:
        verbose_name = "配送区域"
        verbose_name_plural = "DeliveryArea"

    area_name = models.CharField(max_length=150)

    @staticmethod
    def area_all():
        return DeliveryArea.objects.all()

    def __len__(self):
        return len(DeliveryArea.area_all())


class Store(models.Model):
    class Meta:
        verbose_name = "商户"
        verbose_name_plural = "Store"

    pay_type_level = (
        (0, '日结'),
        (1, '月结'),
    )

    # 只有在押金不为0时此选项才有意义
    despoit_level = (
        (0, '押金已付'),
        (1, '押金未付')
    )

    store_id = models.IntegerField(
        primary_key=True
    )
    store_name = models.CharField(
        max_length=155,
        default=0
    )
    store_phone = models.BigIntegerField(
        default=0
    )
    store_addr = models.CharField(
        max_length=150,
        default='无'
    )
    store_area = models.ForeignKey(
        DeliveryArea,
        on_delete=models.CASCADE
    )
    store_pay_type = models.IntegerField(
        default=0,
        choices=pay_type_level
    )
    store_deposit = models.IntegerField(
        default=0
    )
    has_deposit = models.IntegerField(
        default=0,
    )

    @staticmethod
    def store_all():
        return Store.objects.all()

    def __len__(self):
        return len(Store.store_all())

    def info(self):
        return {'id': self.store_id,
                'name': self.store_name,
                'area': self.store_area.id,
                'area_name': self.store_area.area_name,
                'phone': self.store_phone,
                'addr': self.store_addr,
                'deposite': self.store_deposit,
                'pay_type': self.store_pay_type}

    def price(self):
        all_store_price = StoreGoods.objects.filter(store=self)
        result = []
        for i in all_store_price:
            if i.goods.goods_id <= 0:
                continue
            t_info = i.goods.info()
            t_info['goods_price'] = float(i.goods_price)
            t_info['goods_store_stock'] = i.goods_stock

            result.append(t_info)

        return result


class CustomerProfile(models.Model):

    class Meta:
        verbose_name = "顾客资料"
        verbose_name_plural = "CustomerProfiles"

    wk = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.wk)


class PeisongProfile(models.Model):

    class Meta:
        verbose_name = "配送员资料"
        verbose_name_plural = "PeisongProfile"

    wk = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    area = models.ForeignKey(
        DeliveryArea,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        default='peisong_name',
        max_length=50
    )
    phone = models.BigIntegerField(
        default=0
    )

    def __str__(self):
        return str(self.wk)


class Goods(models.Model):

    class Meta:
        verbose_name = "商品列表"
        verbose_name_plural = "Goodss"

    def info(self):
        return {'goods_id': self.goods_id,
                'goods_name': self.goods_name,
                'goods_spec': self.goods_spec,
                'goods_stock': self.goods_stock,
                'is_recover': self.is_recover,
                'goods_type': self.goods_type,
                'goods_img': 'https://test-12345-1252731440.cosbj.myqcloud.com/' + self.goods_img}

    recover_level = (
        (0, '回收'),
        (1, '不回收')
    )
    goods_type_choice = (
        (0, '出售品'),
        (1, '消耗品')
    )
    goods_id = models.AutoField(
        primary_key=True
    )
    goods_img = models.CharField(
        max_length=155,
        null=True,
        default='wx5c7d55175f3872b7.o6zAJs8x6UgW6Y0lRp1jPSO_gcUA.3x4A1YBcSFlHdc484c27e29d772bb6cb9b96aa76ebcc.jpg'
    )
    goods_name = models.CharField(
        max_length=155,
        default='not name'
    )
    goods_spec = models.CharField(
        max_length=255,
        default=0
    )
    goods_stock = models.IntegerField(
        default=0
    )
    goods_type = models.IntegerField(
        default=0
    )
    is_recover = models.IntegerField(
        default=0,
        choices=recover_level
    )

    @staticmethod
    def goods_all(is_all=0):
        if is_all == 0:
            return Goods.objects.all()
        else:
            return Goods.objects.filter(goods_type=0)


class PeisongCarStock(models.Model):
    goods_type_choice = (
        (0, '新货'),
        (1, '旧货')
    )

    def info(self):
        info = self.goods.info()
        info['goods_stock'] = int(self.goods_stock)
        return info

    class Meta:
        verbose_name = "配送员车上货物"
        verbose_name_plural = "PeisongCarStocks"

    wk = models.ForeignKey(
        PeisongProfile,
        on_delete=models.CASCADE
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.SET(-2)
    )
    goods_stock = models.IntegerField(
        default=0
    )
    goods_type = models.IntegerField(
        default=0,
        choices=goods_type_choice
    )


class StoreGoods(models.Model):

    class Meta:
        verbose_name = "商户货物"
        verbose_name_plural = "StoreGoodss"

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.SET(-2)
    )
    goods_stock = models.IntegerField(
        default=0
    )
    goods_price = models.DecimalField(
        max_digits=8,
        decimal_places=3
    )


class Order(models.Model):

    class Meta:
        verbose_name = "商户订单"
        verbose_name_plural = "Orders"
        ordering = ['-create_time']

    def get_order_detail(self):
        return OrderDetail.objects.filter(order_id=self.order_id)

    def info(self):
        return {
            'order_id': str(self.order_id),
            'create_time': str(self.create_time),
            'create_timestamp': time.mktime(self.create_time.timetuple()),
            'order_type': self.order_type,
            'pay_type': self.pay_type,
            'order_total_price': str(self.order_total_price),
            'receive_time': str(self.receive_time),
            'pay_from': self.pay_from,
            'remarks': self.order_remarks,
            'done_time': str(self.done_time),
            'ps_user':str(self.ps_user),
            'create_user': str(self.user),
            'done_user': str(self.done_user) if self.done_user else 'None'
        }

    def goods_info(self):
        result = []
        goods = OrderDetail.objects.filter(order_id=self.order_id)

        for i in goods:
            result.append({'goods_id': i.goods.goods_id,
                           'goods_name': i.goods.goods_name,
                           'goods_spec': i.goods.goods_spec,
                           'goods_count': i.goods_count,
                           'total_price': str(i.total_price)})

        return result

    pay_type_level = (
        (0, '日结'),
        (1, '月结')
    )
    order_type_level = (
        (0, '已完成'),
        (1, '待支付'),
        (2, '待送达'),
        (3, '已取消')
    )
    pay_from_level = (
        (0, '现金'),
        (1, '微信'),
        (2, '月结'),
        (3, '未支付')
    )

    order_id = models.BigIntegerField(
        primary_key=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        DeliveryArea,
        on_delete=models.CASCADE
    )
    ps_user = models.ForeignKey(
        PeisongProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    order_type = models.IntegerField(
        choices=order_type_level,
        default=2
    )
    receive_time = models.DateTimeField(
        null=True,
        blank=True
    )
    pay_type = models.IntegerField(
        choices=pay_type_level,
        default=0
    )
    pay_from = models.IntegerField(
        choices=pay_from_level,
        default=3
    )
    order_total_price = models.DecimalField(
        max_digits=8,
        decimal_places=3
    )
    order_remarks = models.CharField(
        max_length=155
    )
    done_time = models.DateTimeField(
        null=True,
        blank=True
    )
    done_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class OrderDetail(models.Model):

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = "OrderDetails"

    order_id = models.BigIntegerField(null=True)

    goods = models.ForeignKey(
        Goods,
        on_delete=models.SET(-2)
    )
    goods_count = models.IntegerField()
    goods_price = models.DecimalField(
        max_digits=8,
        decimal_places=3
    )
    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=3
    )


class PickOrder(models.Model):

    class Meta:
        verbose_name = "领货订单"
        verbose_name_plural = "PickOrders"
        ordering = ['-create_time']

    def get_order_detail(self):
        return PickOrderDetail.objects.filter(order_id=self.order_id)

    def info(self):
        return {
            'order_id': str(self.order_id),
            'create_time': str(self.create_time),
            'order_type': self.order_type,
            'order_status': self.order_status,
            'pick_user': self.pick_user.name,
            'confirm_time': str(self.confirm_time),
            'is_modify': self.is_modify
        }

    def goods_info(self):
        result = []
        goods = PickOrderDetail.objects.filter(order_id=self.order_id)

        for i in goods:
            result.append({'goods_id': i.goods.goods_id,
                           'goods_name': i.goods.goods_name,
                           'goods_spec': i.goods.goods_spec,
                           'goods_count': i.goods_count})

        return result

    modify_level = (
        (0, '未被修改'),
        (1, '被修改')
    )
    order_type_level = (
        (0, '领货订单'),
        (1, '回库订单')
    )
    order_status_level = (
        (0, '已确认'),
        (1, '未确认')
    )

    order_id = models.BigIntegerField(
        primary_key=True
    )
    order_status = models.IntegerField(
        choices=order_status_level,
        default=1
    )
    order_type = models.IntegerField(
        choices=order_type_level,
        default=0
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    pick_user = models.ForeignKey(
        PeisongProfile,
        on_delete=models.CASCADE
    )
    confirm_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE
    )
    confirm_time = models.DateTimeField(
        null=True,
        blank=True
    )
    is_modify = models.IntegerField(
        default=0
    )


class PickOrderDetail(models.Model):

    class Meta:
        verbose_name = "PickOrderDetail"
        verbose_name_plural = "PickOrderDetails"


    order_id = models.BigIntegerField(null=True)
    goods = models.ForeignKey(
        Goods,
        on_delete=models.SET(-2)
    )
    goods_count = models.IntegerField()


class RecoverOrder(models.Model):
    order_type_level = (
        (0, '已完成'),
        (1, '待取货'),
        (2, '已取消')
    )

    class Meta:
        verbose_name = "RecoverOrder"
        verbose_name_plural = "RecoverOrders"

    def info(self):
        return {
            'order_id': str(self.order_id),
            'order_type': self.order_type,
            'create_time': str(self.create_time),
            'create_timestamp': time.mktime(self.create_time.timetuple()),
            'ps_user': str(self.ps_user),
            'receive_time': self.receive_time,
            'store_name': self.store.store_name,
            'store_phone': self.store.store_phone,
            'store_addr': self.store.store_addr,
        }

    def goods_info(self):
        result = []
        goods = RecoverModelDetail.objects.filter(order_id=self.order_id)

        for i in goods:
            result.append({'goods_id': i.goods.goods_id,
                           'goods_name': i.goods.goods_name,
                           'goods_spec': i.goods.goods_spec,
                           'goods_count': i.goods_count})

        return result

    order_id = models.BigIntegerField(
        primary_key=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE
    )
    area = models.ForeignKey(
        DeliveryArea,
        on_delete=models.CASCADE
    )
    ps_user = models.ForeignKey(
        PeisongProfile,
        on_delete=models.CASCADE,
        null=True
    )
    order_type = models.IntegerField(
        choices=order_type_level,
        default=1
    )
    receive_time = models.DateTimeField(
        null=True,
        blank=True
    )


class RecoverModelDetail(models.Model):

    class Meta:
        verbose_name = "RecoverModelDetail"
        verbose_name_plural = "RecoverModelDetails"

    order_id = models.BigIntegerField(
        null=True
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.SET(-2)
    )

    goods_count = models.IntegerField()


class Session(models.Model):
    session_key = models.CharField(
        max_length=100,
        primary_key=True
    )
    session_data = models.CharField(
        max_length=100,
        unique=True
    )
    we_ss_key = models.CharField(
        max_length=100,
        default='None',
    )
    expire_date = models.DateTimeField()


class CodeRecord(models.Model):
    code_key = models.IntegerField(
        primary_key=True
    )
    code_name = models.CharField(
        max_length=100,
        default='not defined',
    )
    code_count = models.IntegerField(
        default=0
    )


class AdBanner(models.Model):
    """docstring for AdBanner"""
    # b_titie = models.CharField(
    #     max_length=100
    # )
    b_img = models.CharField(
        max_length=155,
        default=0,
        null=True,
    )

    @staticmethod
    def all():
        return [{'id': i.id, 'img': i.b_img} for i in AdBanner.objects.all()]


class AdContent(models.Model):
    """docstring for AdContent"""
    c_title = models.CharField(
        max_length=100
    )
    c_img = models.CharField(
        max_length=155,
        default=0,
        null=True,
    )
    c_content = models.CharField(
        max_length=155,
        default=0,
        null=True,
    )

    @staticmethod
    def all():
        return [{'id': i.id, 'title': i.c_title, 'content': i.c_content, 'img': i.c_img} for i in AdContent.objects.all()]
