from django.contrib import admin
from django.urls import path
from .views import update_products_view
from .models import Product, OrderItem, Order, Brand, Page, PageCategory, ProductType, Customer, ShippingAddress, \
                    Series, Technology, PaymentType, DeliveryType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('art_code', 'name', 'brand', 'price', 'series', 'technology', 'is_active', 'in_stock',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update-products/', self.admin_site.admin_view(update_products_view), name='update_products'),
        ]
        return custom_urls + urls


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

    def price(self, obj):
        return obj.product.price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('customer', 'complete', 'created', 'updated', 'get_cart_total', 'get_address',)
    list_display = ('customer',  'created', 'updated', 'complete', 'get_cart_total', 'payment_type', 'delivery_type',)
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
