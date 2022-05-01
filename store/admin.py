from django.contrib import admin

from users.models import CustomUser

# Register your models here.

from .models import Order,OrderItem

admin.site.register(OrderItem)


class OrderItemTabularInline(admin.TabularInline):

    model = OrderItem
    extra = 0
    can_delete = False
    can_edit = False


class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderItemTabularInline]

    def get_qty(self,order):
        qty = 0
        for orderItem in order.orderitems.all():
            qty += orderItem.qty
        return f"{qty} товаров"

    def get_user(self,order):
        qty = 0
        if order.status != 'ожидает':
            return f"{order.owner.fullname} - Телефон номера {order.owner.phone}" 
        return "Пользователь все еще выберает товар"

    list_display  = ('get_qty','status','get_user')
    
    fields = (
        'owner',
        'session_id',
        'status',
    )


admin.site.register(Order,OrderAdmin)