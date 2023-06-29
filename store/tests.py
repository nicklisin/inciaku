from django.test import TestCase
from .models import Brand


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
