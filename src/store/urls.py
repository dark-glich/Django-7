from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('home/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.UpdateItem, name="update_item"),
    path('proccess_order/', views.ProcessOrder, name="proccess_order")
]
