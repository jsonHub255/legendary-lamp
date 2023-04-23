from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product, Supplier, Order, OrderItem, Invoice, Vehicle, Driver, ReparationProduct
from .serializers import (ProductSerializer, SupplierSerializer, OrderSerializer,
                          OrderItemSerializer, InvoiceSerializer, VehicleSerializer, DriverSerializer, ReparationProductListCreateSerializer, ReparationProductRetrieveUpdateDestroySerializer)

from django.contrib.auth.decorators import login_required
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from .models import UserProfile



# Create your views here.

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    fields = '__all__'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

# Product views
class ProductListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

# Supplier views
class SupplierListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

class SupplierDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

# Order views
class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderCreateAPIView(generics.CreateAPIView):   
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

# OrderItem views
class OrderItemListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class OrderItemDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class OrderItemCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class OrderItemUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class OrderItemDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

# Invoice views
class InvoiceDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

# Vehicle views
class VehicleListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

class VehicleDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

# Driver views
class DriverListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()

class DriverDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class ReparationProductListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReparationProduct.objects.all()
    serializer_class = ReparationProductListCreateSerializer

    def perform_create(self, serializer):
        # Automatically set the driver to the current user
        serializer.save()
    def get_permissions(self):
        print("Using permissions:", self.permission_classes)
        return super().get_permissions()


class ReparationProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReparationProduct.objects.all()
    serializer_class = ReparationProductRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Recalculate the total price when quantity or product changes
        if 'quantity' in serializer.validated_data or 'product' in serializer.validated_data:
            instance = serializer.save()
            instance.total_price = instance.product.unit_price * instance.quantity
            instance.save()

class ReparationProductListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReparationProduct.objects.all()
    serializer_class = ReparationProductListCreateSerializer
