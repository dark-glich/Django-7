from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
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
        try:
            cart = json.loads(request.COOKIES['FruitStore'])
        except:
            cart = {}
        
        items = []
        order = {'get_cart_total': 00.00, 'get_cart_item': 0, 'shipping':False}
        total_items = order['get_cart_item']
        
        for i in cart:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['q'])
            order['get_cart_total'] += total 
            total_items += cart[i]['q']
            
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price':product.price,
                    'ImageURL': product.ImageURL
                },
                'quantity': cart[i]['q'],
                'get_total': total
            }
            items.append(item)

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
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
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
    