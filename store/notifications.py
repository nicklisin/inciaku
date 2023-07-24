import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OrderItem


def send_order_notification_to_managers(order, recipients):
    order_items = list(OrderItem.objects.filter(order=order))
    subject = 'Новый заказ на сайте'
    body = render_to_string('emails/order_notification_manager_body.txt', {
        'order_number': order.id,
        'customer_name': order.customer.name,
        'customer_email': order.customer.email,
        'order_total': order.get_cart_total,
        'order_items': order_items,
    })
    plain_text_body = strip_tags(body)

    send_mail(subject, plain_text_body, os.environ.get('DEFAULT_FROM_EMAIL'), recipients, html_message=body)


def send_order_confirmation_to_customer(order):
    order_items = list(OrderItem.objects.filter(order=order))
    subject = 'Ваш заказ получен'
    body = render_to_string('emails/order_confirmation_body.txt', {
        'customer_name': order.customer.name,
        'order_number': order.id,
        'order_date': order.created,
        'order_total': order.get_cart_total,
        'order_items': order_items,
    })

    send_mail(subject, body, os.environ.get('DEFAULT_FROM_EMAIL'), [order.customer.email])
