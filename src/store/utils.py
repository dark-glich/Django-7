import json
from .models import *

def CookieCart(request):
     try:
          cart = json.loads(request.COOKIES['FruitStore'])
     except:
          cart = {}
     items = []
     order = {'get_cart_total': 00.00, 'get_cart_item': 0, 'shipping':False}
     total_items = order['get_cart_item']
     try:
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
     except:
          pass   
        
     return {'items':items, 'order':order, 'total_items':total_items}

def cartData(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, complete = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          total_items = 0
          for item in items:
               total_items += 1 
     else:
          CookieData = CookieCart(request)
          items = CookieData['items']
          order = CookieData['order']
          total_items = CookieData['total_items']
     return {'items':items, 'order':order, 'total_items':total_items}

def GuestOrder(request, data):
     name = data['form']['name']
     email = data['form']['email']
     cookieData = CookieCart(request)
     items = cookieData['items']
     customer, created = Customer.objects.get_or_create(email=email)
     customer.name = name
     customer.save()
     order, complete = Order.objects.get_or_create(customer=customer, complete=False)
     
     for item in items:
          product = Product.objects.get(id=item['product']['id'])
          orer_item = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])
          
     return customer, order
          