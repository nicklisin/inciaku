# from django.template.loader import render_to_string
from django.test import TestCase
# from django.core import mail
from .models import Brand
from store.notifications import send_order_notification_to_managers
from unittest.mock import patch, Mock


class ModelTesting(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Inci Aku')

    def test_brand_model(self):
        d = self.brand
        self.assertTrue(isinstance(d, Brand))
        self.assertEqual(str(d), 'Inci Aku')

    def test_index_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class NotificationTesting(TestCase):

    @patch('store.models.OrderItem.objects.filter')
    @patch('store.notifications.send_mail')
    def test_send_order_notification_to_managers(self, mock_send_mail, mock_filter):

        # Arrange
        mock_order = Mock()
        mock_order.id = 123
        mock_order.customer.name = 'John Doe'
        mock_order.customer.email = 'customer@email.com'
        mock_order.get_cart_total = 10000

        mock_order_item1 = Mock()
        mock_order_item2 = Mock()

        mock_filter.return_value = [mock_order_item1, mock_order_item2]

        expected_recipients = ['manager1@example.com', 'manager2@example.com']

        # Act
        send_order_notification_to_managers(mock_order, expected_recipients)

        # Assert
        self.assertTrue(mock_send_mail.called)
        actual_recipients = mock_send_mail.call_args[0][3]
        self.assertEqual(set(expected_recipients), set(actual_recipients))

        self.assertEqual(mock_send_mail.call_args[0][0], 'Новый заказ на сайте')
        self.assertIn(str(mock_order.id), mock_send_mail.call_args[0][1])
        self.assertIn(mock_order.customer.name, mock_send_mail.call_args[0][1])
        self.assertIn(mock_order.customer.email, mock_send_mail.call_args[0][1])
        self.assertIn(str(mock_order.get_cart_total), mock_send_mail.call_args[0][1])

        # # Call function to render email body
        # body = render_to_string('emails/order_notification_manager_body.txt', {
        #     'order_number': mock_order.id,
        #     'customer_name': mock_order.customer.name,
        #     'customer_email': mock_order.customer.email,
        #     'order_total': mock_order.get_cart_total,
        #     'order_items': [mock_order_item1, mock_order_item2],
        # })
        #
        # # Assertions
        # assert mock_order.id in body
        # assert mock_order.customer.name in body
        # assert str(mock_order.get_cart_total) in body
        # assert str(mock_order_item1) in body
        # assert str(mock_order_item2) in body


"""
class OrderNotificationTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john.doe@example.com',
            total=100.0,
            # Дополнительные поля заказа, если необходимо
        )

    def test_send_order_confirmation_to_customer(self):
        # Проверяем, что уведомление для клиента отправляется правильно

        # Отправляем уведомление
        send_order_confirmation_to_customer(self.order)

        # Проверяем, что уведомление было отправлено
        self.assertEqual(len(mail.outbox), 1)

        # Проверяем, что тема уведомления правильная
        self.assertIn('Order Confirmation: Order #', mail.outbox[0].subject)

        # Проверяем, что получатель уведомления указан верно
        self.assertEqual(mail.outbox[0].recipients(), [self.order.customer_email])

        # Проверяем, что тело уведомления содержит правильные данные заказа
        self.assertIn(str(self.order.order_number), mail.outbox[0].body)
        self.assertIn(self.order.customer_name, mail.outbox[0].body)
        self.assertIn(str(self.order.total), mail.outbox[0].body)
        # Дополнительные проверки для других полей заказа

    def test_order_confirmation_email_html_content(self):
        # Проверяем, что уведомление для клиента содержит HTML контент

        # Отправляем уведомление
        send_order_confirmation_to_customer(self.order)

        # Получаем HTML содержимое уведомления
        html_content = mail.outbox[0].alternatives[0][0]

        # Проверяем, что HTML содержит правильные данные заказа
        self.assertIn(str(self.order.order_number), html_content)
        self.assertIn(self.order.customer_name, html_content)
        self.assertIn(str(self.order.total), html_content)
        # Дополнительные проверки для других полей заказа

        # Проверяем, что HTML содержит правильные теги и форматирование
        self.assertIn('<html>', html_content)
        self.assertIn('<body>', html_content)
        self.assertIn('</body>', html_content)
        self.assertIn('</html>', html_content)

        # Здесь можно добавить другие проверки для HTML содержимого уведомления
"""
