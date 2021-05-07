from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

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


def UpdateItem(request):
    data = json.loads(request.body.decode("utf-8"))
    productID = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(product=product, order=order)
    
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    
    orderitem.save()
    
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item Added', safe=False)

def ProcessOrder(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data['shippingInfo'])
    return JsonResponse('Item Added', safe=False)
    