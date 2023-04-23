from rest_framework import serializers
from .models import Product, Supplier, Order, OrderItem, Invoice, Vehicle, Driver, ReparationProduct, ReparationInvoice, ReparationProductItem



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'SKU', 'name', 'reference', 'unit_price', 'items_per_unit','current_quantity']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'date_ordered', 'date_delivered', 'is_delivered', 'total_price', 'status', 'delivery_order_number', 'supplier', 'products']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'



# serializers.py
class ReparationProductItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ReparationProductListCreateSerializer(serializers.ModelSerializer):
    products = ReparationProductItemSerializer(many=True)

    class Meta:
        model = ReparationProduct
        fields = ['id', 'vehicle', 'odometer', 'products', 'date_repaired', 'location', 'driver', 'total_price']
    
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        reparation_product = ReparationProduct.objects.create(**validated_data)
        for product_data in products_data:
            ReparationProductItem.objects.create(reparation_product=reparation_product, **product_data)
        return reparation_product

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products')
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.odometer = validated_data.get('odometer', instance.odometer)
        instance.date_repaired = validated_data.get('date_repaired', instance.date_repaired)
        instance.location = validated_data.get('location', instance.location)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.save()
        product_items = instance.reparationproductitem_set.all()
        product_items.delete()
        for product_data in products_data:
            ReparationProductItem.objects.create(reparation_product=instance, **product_data)
        instance.refresh_from_db()
        return instance



class ReparationProductRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    products = ReparationProductItemSerializer(many=True)

    class Meta:
        model = ReparationProduct
        fields = ['id', 'vehicle', 'odometer', 'products', 'date_repaired', 'location', 'driver', 'total_price']
        read_only_fields = ['id', 'total_price']

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products')
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.odometer = validated_data.get('odometer', instance.odometer)
        instance.date_repaired = validated_data.get('date_repaired', instance.date_repaired)
        instance.location = validated_data.get('location', instance.location)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.save()
        product_items = instance.reparationproductitem_set.all()
        product_items.delete()
        for product_data in products_data:
            ReparationProductItem.objects.create(reparation_product=instance, **product_data)
        instance.refresh_from_db()
        return instance