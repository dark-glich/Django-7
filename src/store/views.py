from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, complete = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_items = 0
        for item in items:
            total_items += 1
    else:
        items = []
        order = {'get_cart_total': 00.00}
        total_items = 0 

    context = {'items':items, 'order': order, 'total_items':total_items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, complete = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_items = 0
        for item in items:
            total_items += 1 
    else:
        items = []
        order = {'get_cart_total': 00.00}
        total_items = 0 

    context = {'items':items, 'order': order, 'total_items':total_items}
    return render(request, 'store/checkout.html', context)