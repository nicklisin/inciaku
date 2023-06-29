from .models import Order, Page
from .utils import cookie_cart


def cart_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        count = order.get_cart_count
    else:
        count = cookie_cart(request)['cart_count']
    return {'cart_count_global': count}


def get_main_menu(request):
    main_menu = Page.objects.filter(in_main_menu=True).order_by('-order')
    return {'main_menu': main_menu}
