from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from inventory.views import (
    ProductListAPIView,
    ProductDetailAPIView,
    SupplierListAPIView,
    SupplierDetailAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    OrderCreateAPIView,
    OrderUpdateAPIView,
    OrderDeleteAPIView,
    OrderItemListAPIView,
    OrderItemDetailAPIView,
    OrderItemCreateAPIView,
    OrderItemUpdateAPIView,
    OrderItemDeleteAPIView,
    InvoiceDetailAPIView,
    VehicleListAPIView,
    VehicleDetailAPIView,
    DriverListAPIView,
    DriverDetailAPIView,
    ReparationProductListCreateAPIView,
    ReparationProductRetrieveUpdateDestroyAPIView,
    ReparationProductListAPIView,
)

urlpatterns = [
    # Product urls
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),

    # Supplier urls
    path('suppliers/', SupplierListAPIView.as_view(), name='supplier_list'),
    path('suppliers/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier_detail'),

    # Order urls
    path('orders/', OrderListAPIView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateAPIView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', OrderUpdateAPIView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteAPIView.as_view(), name='order_delete'),

    # OrderItem urls
    path('orderitems/', OrderItemListAPIView.as_view(), name='order_item_list'),
    path('orderitems/create/', OrderItemCreateAPIView.as_view(), name='order_item_create'),
    path('orderitems/<int:pk>/', OrderItemDetailAPIView.as_view(), name='order_item_detail'),
    path('orderitems/<int:pk>/update/', OrderItemUpdateAPIView.as_view(), name='order_item_update'),
    path('orderitems/<int:pk>/delete/', OrderItemDeleteAPIView.as_view(), name='order_item_delete'),

    # Invoice urls
    path('invoices/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice_detail'),

    # Vehicle urls
    path('vehicles/', VehicleListAPIView.as_view(), name='vehicle_list'),
    path('vehicles/<int:pk>/', VehicleDetailAPIView.as_view(), name='vehicle_detail'),

    # Driver urls
    path('drivers/', DriverListAPIView.as_view(), name='driver_list'),
    path('drivers/<int:pk>/', DriverDetailAPIView.as_view(), name='driver_detail'),

    # Reparation urls
    path('reparation_products/create/', ReparationProductListCreateAPIView.as_view(), name='reparation_product_list_create'),
    path('reparation_products/<int:pk>/', ReparationProductRetrieveUpdateDestroyAPIView.as_view(), name='reparation_product_retrieve_update_destroy'),
    path('reparation_products/list/', ReparationProductListAPIView.as_view(), name='reparation_product_list'),
]



urlpatterns = format_suffix_patterns(urlpatterns)
