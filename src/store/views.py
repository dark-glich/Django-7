from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import CookieCart, cartData, GuestOrder

def store(request):
    products = Product.objects.all().order_by('-date_added')
    context = {'products': products}
    
    
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    total_items = data['total_items']

    context = {'items':items, 'order': order, 'total_items':total_items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    total_items = data['total_items']

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
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    
    orderitem.save()
    
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item Added', safe=False)

def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data = json.loads(request.body.decode("utf-8"))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, complete = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = GuestOrder(request, data)
    total = float(data['form']['get_total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.save()
    
    ShippingAdress.objects.create(
        customer=customer, 
        order=order,
        adrress= data['shippingInfo']['address'],
        city= data['shippingInfo']['city'],
        state= data['shippingInfo']['state'],
        zipcode= data['shippingInfo']['zipcode'],
    )
    
    
    return JsonResponse('Item Added', safe=False)
    