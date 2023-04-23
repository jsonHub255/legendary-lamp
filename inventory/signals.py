from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, Invoice, Product
from django.contrib.auth.models import User
from .models import UserProfile
import uuid

@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        # If a new order is created, create a corresponding invoice
        invoice_number = 'INV-' + str(instance.id)
        invoice = Invoice(order=instance, invoice_number=invoice_number)
        invoice.save()


