import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Product, Order, OrderItem, ShippingAddress, Page, DeliveryType, PaymentType
from .utils import cookie_cart, cart_data, guest_order, get_meta, get_filter_params


def index(request):
    data = {}
    meta = get_meta(request, 'index', None)
    context = {'data': data, 'meta': meta}
    return render(request, 'store/index.html', context=context)


def text_page(request, url):
    page = get_object_or_404(Page, url=url)
    if page:
        meta = get_meta(request, 'text_page', page)
        context = {'page': page, 'meta': meta}
        return render(request, 'store/text_page.html', context=context)


def store(request):
    data = cart_data(request)
    meta = get_meta(request, 'store', data)
    items = data['items']
    items_ids = []
    # TODO вернуть список айдишников (не работает при авторизации)
    # for i in items:
    #     items_ids.append(i['product']['id'])
    filter_params = get_filter_params(request)
    products = Product.objects.all()

    filter_polarities = products.distinct().values('polarity')
    polarities_choices = Product.polarity.field.choices
    polarities_choices_clear = []
    for i in filter_polarities:
        polarities_choices_clear.append(i['polarity'])
    res = []
    for i in polarities_choices:
        if i[0] in polarities_choices_clear:
            res.append([i[0], i[1]])

    if filter_params['polarity']:
        products = products.filter(polarity__in=filter_params['polarity'])
    if filter_params['capacity_from']:
        capacity_from = filter_params['capacity_from'] or 0
        capacity_to = filter_params['capacity_to'] or 300
        products = products.filter(Q(capacity__gte=capacity_from) & Q(capacity__lte=capacity_to))

    context = {'products': products, 'items': items, 'items_ids': items_ids, 'meta': meta, 'filter_polarities': res}
    return render(request, 'store/store.html', context)


def item(request, slug):
    product_item = Product.objects.select_related('brand', 'technology', 'type', 'technology').get(slug=slug)
    meta = get_meta(request, 'item', product_item)
    context = {'product': product_item, 'meta': meta}
    return render(request, 'store/item.html', context)


def cart(request):
    data = cart_data(request)
    meta = get_meta(request, 'cart', None)
    delivery_types = DeliveryType.objects.all()
    payment_types = PaymentType.objects.all()
    items = data['items']
    get_cart_total = data['cart_total']
    get_cart_count = data['cart_count']
    customer = data['customer']
    context = {'customer': customer, 'items': items, 'cart_total': get_cart_total, 'cart_count': get_cart_count,
               'delivery_types': delivery_types, 'payment_types': payment_types, 'meta': meta}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    get_cart_total = data['cart_total']
    get_cart_count = data['cart_count']
    customer = data['customer']

    context = {'customer': customer, 'items': items, 'cart_total': get_cart_total, 'cart_count': get_cart_count}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    action = data['action']
    product_id = data['productId']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
        order_item.save()
    if action == 'reduce-q':
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
    if action == 'remove':
        order_item.delete()
    cart_quantity = order.get_cart_count

    return JsonResponse({
        'action': action,
        'product_id': product_id,
        'cart_quantity': cart_quantity
    }, safe=False)


def process_order(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
    else:
        customer, order = guest_order(request, data)

    if data['form']['address']:
        shipping = ShippingAddress.objects.create(customer=customer, order=order)
        shipping.address = data['form']['address']
        shipping.save()
    delivery = DeliveryType.objects.get(id=data['form']['delivery_type'])
    order.delivery_type = delivery
    payment = PaymentType.objects.get(id=data['form']['payment_type'])
    order.payment_type = payment
    order.save()

    return JsonResponse('order submitted', safe=False)


def get_guest_cart_total(request):
    cookie_data = cookie_cart(request)
    cookie_cart_total = cookie_data['cart_total']
    return JsonResponse(cookie_cart_total, safe=False)


def thanks(request):
    return render(request, 'store/thanks.html')


def handle_404(request, exception):
    return render(request, '404.html')
