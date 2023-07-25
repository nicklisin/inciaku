import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OrderItem
import threading


def send_order_notification_to_managers(order, recipients):
    order_items = list(OrderItem.objects.filter(order=order))
    subject = 'Новый заказ на сайте'
    html_message = render_to_string('emails/order_notification_manager_body.txt', {
        'order_number': order.id,
        'customer_name': order.customer.name,
        'customer_email': order.customer.email,
        'order_total': order.get_cart_total,
        'order_items': order_items,
    })
    message = strip_tags(html_message)
    threading.Thread(target=send_mail,
                     args=(subject,
                           message,
                           os.environ.get('DEFAULT_FROM_EMAIL'),
                           recipients,
                           html_message)).start()


def send_order_confirmation_to_customer(order):
    order_items = list(OrderItem.objects.filter(order=order))
    subject = 'Ваш заказ получен'
    html_message = render_to_string('emails/order_confirmation_body.txt', {
        'customer_name': order.customer.name,
        'order_number': order.id,
        'order_date': order.created,
        'order_total': order.get_cart_total,
        'order_items': order_items,
    })
    message = strip_tags(html_message)
    threading.Thread(target=send_mail,
                     args=(subject,
                           message,
                           os.environ.get('DEFAULT_FROM_EMAIL'),
                           [order.customer.email],
                           False,
                           None,
                           None,
                           None,
                           html_message)).start()
