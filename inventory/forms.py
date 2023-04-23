from django import forms
from .models import Order, Invoice, Vehicle, Driver
from .models import Order, OrderItem
from django.forms import inlineformset_factory
import uuid

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    widgets = {
        'total_price': forms.TextInput(attrs={'readonly': 'readonly'})
    }
)



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'status', 'is_delivered', 'delivery_order_number']




class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['code', 'license_plate', 'brand', 'model', 'year', 'chassis_number', 'engine_model']


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'phone', 'driving_license']
