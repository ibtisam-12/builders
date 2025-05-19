# ecommerce/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ecommerce_view, {'page_type': 'home'}, name='home'),  # Homepage view
    path('product/<slug:product_slug>/', views.ecommerce_view, {'page_type': 'product_detail'}, name='product_detail'),  # Product detail page
    path('add_to_cart/<slug:product_slug>/', views.ecommerce_view, {'page_type': 'add_to_cart'}, name='add_to_cart'),  # Add to cart
    path('cart/', views.ecommerce_view, {'page_type': 'view_cart'}, name='view_cart'),  # View cart page
    path('checkout/', views.ecommerce_view, {'page_type': 'checkout'}, name='checkout'),  # Checkout page
    path('gym-equipment/', views.equipment, name='equipment'),  # Equipment page
    path('apparel/', views.apparel, name='apparel'),  # Apparel page
    path('supplements/', views.supplements, name='supplements'),  # Supplements page
    path('contact/', views.contact, name='contact'),
]
