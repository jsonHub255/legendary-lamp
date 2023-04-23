from django.contrib import admin
from .models import Supplier, Product, Order, OrderItem, Invoice, Vehicle, Driver, UserProfile, ReparationProduct, ReparationProductItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'status', 'is_delivered', 'delivery_order_number')
    list_filter = ('status', 'is_delivered')
    search_fields = ('id', 'supplier__name', 'delivery_order_number')
    inlines = [OrderItemInline]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'invoice_number')
    list_filter = ('order__status',)
    search_fields = ('id', 'order__id', 'invoice_number')


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'license_plate', 'brand', 'model', 'year', 'chassis_number', 'engine_model')
    search_fields = ('id', 'code', 'license_plate')


class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'driving_license')
    search_fields = ('id', 'name', 'phone', 'driving_license')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address')


class ReparationProductItemInline(admin.TabularInline):
    model = ReparationProductItem


class ReparationProductAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date_repaired', 'total_price')
    search_fields = ('vehicle__make', 'vehicle__model', 'location')
    list_filter = ('date_repaired',)
    inlines = [ReparationProductItemInline]


class ReparationProductItemAdmin(admin.ModelAdmin):
    list_display = ('reparation_product', 'product', 'quantity')
    search_fields = ('reparation_product__vehicle__make', 'reparation_product__vehicle__model', 'product__name')
    list_filter = ('product',)


admin.site.register(ReparationProduct, ReparationProductAdmin)
admin.site.register(ReparationProductItem, ReparationProductItemAdmin)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Driver, DriverAdmin)



