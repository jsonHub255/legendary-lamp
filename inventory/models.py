import datetime as dt
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk:
            # check if a UserProfile with the same user_id already exists
            if UserProfile.objects.filter(user_id=self.user_id).exists():
                raise ValueError('A UserProfile with this User already exists.')
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



class Product(models.Model):
    name = models.CharField(max_length=100)
    reference = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    items_per_unit = models.IntegerField(default=1)
    min_quantity = models.IntegerField()
    low_quantity = models.IntegerField()
    current_quantity = models.IntegerField(default=0)
    SKU = models.CharField(max_length=50, editable=False, blank=True)

    # Override the save method to generate a unique SKU SKu is a mix of the first 3 letters of the product name and 3 numbers derived from the reference and 4 numbers derived from 
    def save(self, *args, **kwargs):
        if not self.SKU:
            sku_prefix = self.name[:3].upper()
            ref_numbers = ''.join(filter(str.isdigit, self.reference))[-3:]
            rand_numbers = str(uuid.uuid4().int)[:4]
            self.SKU = f"{sku_prefix}{ref_numbers}{rand_numbers}"
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return self.name + ' - ' + self.SKU

# make model for supplier
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_choices = (
        ('P', 'PENDING'),
        ('C', 'COMPLETED'),
        ('CN', 'CANCELLED'),
    )
    status = models.CharField(max_length=150, choices=status_choices, default='P')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # delivery_order_number must be unique and to be updated one status_choices is changed to completed
    delivery_order_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.status == 'C' and self.delivery_order_number:
            # check for uniqueness only when status is "completed"
            existing_order = Order.objects.filter(
                status='C',
                delivery_order_number=self.delivery_order_number
            ).exclude(pk=self.pk).first()
            if existing_order:
                raise ValidationError(
                    {'delivery_order_number': 'Delivery order number must be unique.'}
                )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())[:8].upper()

        if self.is_delivered and self.status != 'C':
            self.status = 'C'
            self.delivery_order_number = str(uuid.uuid4())[:8].upper()

        # Calculate the total price of the order based on the products in the order
        super().save(*args, **kwargs)
        self.total_price = sum([item.product.unit_price * item.quantity for item in self.orderitem_set.all()])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    Order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.pk:
            # If this is a new invoice, calculate the total price
            self.total_price = self.order.total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=50, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    chassis_number = models.CharField(max_length=50, blank=True, null=True)
    engine_model = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# Driver class model to store the driver information and the vehicle he drives
class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    driving_license = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class LatestReparationProductManager(models.Manager):
    def get_latest_reparation_product_for_vehicle(self, vehicle):
        return self.filter(vehicle=vehicle).order_by('-date_created').first()


# generate comment for the class model below
class ReparationProduct(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    odometer = models.IntegerField(blank=True, null=True)
    products = models.ManyToManyField(Product, through='ReparationProductItem')
    date_repaired = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default="Driver not assigned")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Recalculate the total price based on the product quantities
        self.total_price = sum(item.product.unit_price * item.quantity for item in self.reparationproductitem_set.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle} ({self.date_repaired})'

    class Meta:
        unique_together = ('vehicle', 'date_repaired')


class ReparationProductItem(models.Model):
    reparation_product = models.ForeignKey(ReparationProduct, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} ({self.quantity})'



class ReparationInvoice(models.Model):
    reparation = models.OneToOneField(ReparationProduct, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = str(uuid.uuid4())[:8].upper()
        self.total_price = self.reparation.total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number


# make a class for knowing a current quantity of product in the stock by passing the product name and reference
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name

    # FUNCTION the product to be added to the stock and the quantity to be updated but it is not working
    def add_product_to_stock(self, product, quantity):
        stock = self.get_stock_for_product(product)
        stock.quantity += quantity
        stock.save()

    def get_stock_for_product(self, product):
        return self.filter(product=product).first()
    
    # FUNCTION the product to be removed from the stock and the quantity to be updated but it is not working
    def remove_product_from_stock(self, product, quantity):
        stock = self.get_stock_for_product(product)
        stock.quantity -= quantity
        stock.save()

    def get_stock_for_product(self, product):
        return self.filter(product=product).first()

    # FUNCTION to update the stock when a product is added to the stock
    def update_stock(self, product, quantity):
        stock = self.get_stock_for_product(product)
        stock.quantity += quantity
        stock.save()

    
        # run those fuctions in the admin.py file to update the stock when a product is added to the stock
        def save_model(self, request, obj, form, change):
            super().save_model(request, obj, form, change)
            if change:
                self.update_stock(obj.product, obj.quantity)

        def update_stock(self, product, quantity):

            stock = Stock.objects.get_stock_for_product(product)
            stock.quantity += quantity
            stock.save()
        
        @classmethod
        def get_stock_for_product(cls, product):
            stock, created = cls.objects.get_or_create(product=product)
            return stock

# def generate_delivery_order_number():
#     return str(uuid.uuid4())[:8].upper()
