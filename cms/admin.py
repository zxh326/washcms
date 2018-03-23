from django.contrib import admin
from cms.models import CodeRecord, User, CustomerProfile, Store, DeliveryArea, Goods, Order, OrderDetail, StoreGoods
# Register your models here.


class CodeRecordAdmin(admin.ModelAdmin):
    '''
        Admin View for CodeRecord
    '''
    list_display = ('code_key', 'code_name', 'code_count',)
    list_filter = ('code_name',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)


class UserProfileAdmin(admin.StackedInline):
    model = CustomerProfile
    verbose_name = '商家用户信息'
    can_delete = True


class UserTypeFilter(admin.SimpleListFilter):
    title = (u'用户身份')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            (0, u'管理员'),
            (1, u'库管'),
            (2, u'配送员'),
            (3, u'顾客'),
            (4, u'未注册')
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if int(self.value()) == 0:
                return queryset.filter(user_type=0)
            if int(self.value()) == 1:
                return queryset.filter(user_type=1)
            if int(self.value()) == 2:
                return queryset.filter(user_type=2)
            if int(self.value()) == 3:
                return queryset.filter(user_type=3)
            if int(self.value()) == 4:
                return queryset.filter(user_type=4)


class UserAdmin(admin.ModelAdmin):
    '''
        Admin View for User
        edit profile return default
    '''

    def get_user_type(self, user):
        if user.user_type == 0:
            return u'%s' % (u"管理员",)
        elif user.user_type == 2:
            return u'%s' % (u"配送员",)
        elif user.user_type == 3:
            return u'%s' % (u"顾客",)
        elif user.user_type == 1:
            return u'%s' % (u"库管",)
        elif user.user_type == 4:
            return u'%s' % (u"未注册",)

    get_user_type.short_description = u'用户类型'

    get_user_type.allow_tags = True

    def get_readonly_fields(self, *args, **kwargs):
        return ['wk']

    list_display = ('wk', 'nick_name', 'get_user_type','last_login')

    list_filter = (UserTypeFilter,)
    inlines = (UserProfileAdmin,)


class StoreAdmin(admin.ModelAdmin):
    '''
        Admin View for Store
    '''
    list_display = ('store_id', 'store_name', 'store_area', 'store_pay_type')
    list_filter = ('store_pay_type', 'store_area')
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)


class AreaAdmin(admin.ModelAdmin):
    '''
        Admin View for Area
    '''
    list_display = ('id', 'area_name',)


class GoodsAdmin(admin.ModelAdmin):

    list_display = ('goods_name', 'goods_spec', 'goods_stock', 'is_recover',)


class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail
    verbose_name = '订单详情'
    can_delete = True


class OrderAdmin(admin.ModelAdmin):
    def store_name(self,Order):
        return u'%s' % (Order.store.store_name,)

    def area_name(self,Order):
        return u'%s' % (Order.area.area_name,)
    readonly_fields = ('user', 'store', 'area', 'order_id',
                       'create_time', 'done_time', 'order_total_price')

    list_display = ('order_type','create_time', 'store_name', 'pay_type',
                    'pay_from', 'order_total_price','area_name')

    list_filter = ('order_type', 'pay_type','pay_from')

class StoreGoodsAdmin(admin.ModelAdmin):

    def goods_name(self,storegoods):
        return u'%s(%s)' % (storegoods.goods.goods_name,storegoods.goods.goods_spec)

    def store_name(self,storegoods):
        return u'%s' % (storegoods.store.store_name,)

    readonly_fields = ('store', 'goods')
    list_display = ('store_name', 'goods_name', 'goods_price', 'goods_stock')


admin.site.register(StoreGoods, StoreGoodsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(DeliveryArea, AreaAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(CodeRecord, CodeRecordAdmin)
