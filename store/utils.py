import json
from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    get_cart_total = 0
    get_cart_count = 0
    for i in cart:
        try:
            get_cart_count += cart[i]['quantity']
            product = Product.objects.get(id=i)
            item_total = product.price * cart[i]['quantity']
            get_cart_total += item_total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'photoURL': product.photoURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': item_total
            }
            items.append(item)
        except:
            pass
    return {'items': items, 'cart_total': get_cart_total, 'cart_count': get_cart_count}

def cart_data(request):
    customer = 'null'
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all().select_related('product', 'product__brand')
        get_cart_total = order.get_cart_total
        get_cart_count = order.get_cart_count
    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        get_cart_total = cookie_data['cart_total']
        get_cart_count = cookie_data['cart_count']
    return {'customer': customer, 'items': items, 'cart_total': get_cart_total, 'cart_count': get_cart_count}

def guest_order(request, data):
    email = data['form']['email']
    name = data['form']['name']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)
    order.complete = True
    all_cart_data = cart_data(request)
    items = all_cart_data['items']
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])
        order_item.save()
    return customer, order


def get_meta(request, page_type:str, data):
    title = ''
    description = ''
    if page_type == 'index':
        title = 'Inci Aku – Официальный дилер'
        description = 'Официальный дилер Inci Aku в центральном и северо-западном округах.'
    if page_type == 'text_page':
        title = data.title
        description = data.description
    if page_type == 'store':
        title = 'Каталог'
        description = 'Каталог товаров Inci Aku'
    if page_type == 'item':
        title = f'Автомобильный аккумулятор {str(data.brand)} {str(data.name)} {str(data.technology)}'
        try:
            description = str(data.description)
        except:
            pass
    if page_type == 'cart':
        title = 'Корзина'
        description = 'Корзина товаров'

    meta = {
        'title': title,
        'description': description,
    }
    return meta


def get_filter_params(request):
    polarity = []
    capacity_from = 0
    capacity_to = 300
    try:
        polarity = request.GET.getlist('polarity')
    except:
        pass
    try:
        capacity_from = request.GET['capacity-from']
        capacity_to = request.GET['capacity-to']
    except:
        pass
    return {'polarity': polarity, 'capacity_from': capacity_from, 'capacity_to': capacity_to}
