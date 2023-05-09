from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'series', 'technology')


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

    def price(self, obj):
        return obj.product.price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('customer', 'complete', 'created', 'updated', 'get_cart_total', 'get_address',)
    list_display = ('customer',  'created', 'updated', 'complete', 'get_cart_total', 'payment_type', 'delivery_type')
    inlines = [OrderItemsInline]


admin.site.register(Brand)
admin.site.register(Page)
admin.site.register(PageCategory)
admin.site.register(ProductType)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Series)
admin.site.register(Technology)
admin.site.register(PaymentType)
admin.site.register(DeliveryType)





