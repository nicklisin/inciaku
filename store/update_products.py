import os
from django.conf import settings

import requests
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from .models import Product, Brand, get_upload_path
from ecomm1.s3_storage import MediaStorage
from django.core.files.base import ContentFile


def save_photo_from_url(photo_url):
    filename = get_upload_path(None, photo_url.split('/')[-1])  # product/1234567.ext
    response = requests.get(photo_url)
    if response.status_code == 200:
        if settings.DEBUG:
            upload_path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(upload_path, 'wb') as f:
                f.write(response.content)
        else:
            media_storage = MediaStorage(location='media/product')
            photo_content = ContentFile(response.content)
            media_storage.save(filename, photo_content)

    return filename


@dataclass
class ProductFeedItem:
    art_code: str
    # category: str
    # good_type: str
    name: str
    brand: str
    price: int
    length: int
    width: int
    height: int
    cranking_amperage: int
    capacity: int
    polarity: str
    voltage: int
    photo_url: str = ''


@dataclass
class FeedParser:
    feed_url: str

    def parse(self):
        try:
            response = requests.get(self.feed_url)
            response.raise_for_status()  # Вызываем исключение, если код ответа не 200
            xml_data = response.content
            root = ET.fromstring(xml_data)

            products = []

            for item in root.findall('Ad'):
                if str.lower(item.find('Brand').text) == 'inci aku':
                    art_code = item.find('Id').text
                    name = item.find('Title').text
                    brand = item.find('Brand').text
                    price = int(item.find('Price').text)
                    length = int(item.find('Length').text)
                    width = int(item.find('Width').text)
                    height = int(item.find('Height').text)
                    cranking_amperage = int(item.find('DCL').text)
                    capacity = int(item.find('Capacity').text)
                    pol_cont = item.find('Polarity').text
                    if pol_cont == 'Обратная':
                        polarity = 'REV'
                    elif pol_cont == 'Прямая':
                        polarity = 'DIR'
                    else:
                        polarity = 'UNI'
                    voltage = int(item.find('Voltage').text)
                    images = item.find('Images')
                    if 'shop_akb' in images[0].attrib['url']:
                        photo_url = images[0].attrib['url']
                    else:
                        photo_url = ''

                    product = ProductFeedItem(
                        art_code=art_code,
                        # category=category,
                        # good_type=good_type,
                        name=name,
                        brand=brand,
                        price=price,
                        length=length,
                        width=width,
                        height=height,
                        cranking_amperage=cranking_amperage,
                        capacity=capacity,
                        polarity=polarity,
                        voltage=voltage,
                        photo_url=photo_url)
                    products.append(product)

            return products

        except (requests.RequestException, ET.ParseError) as e:
            print(f'Ошибка при получении и разборе фида: {str(e)}')
            return []


class ProductUpdater:
    def __init__(self, feed_parser):
        self.feed_parser = feed_parser

    def update_products(self):
        products_from_feed = self.feed_parser.parse()

        if not products_from_feed:
            # Если список товаров из фида пуст, выходим из метода
            return 0, 0

        updated_count = 0
        added_count = 0
        photos_loaded_count = 0

        for item in products_from_feed:
            try:
                existing_product = Product.objects.get(art_code=item.art_code)
            except Product.DoesNotExist:
                existing_product = None

            if existing_product is not None:
                existing_product.art_code = item.art_code
                # existing_product.category = item.category
                # existing_product.good_type = item.good_type
                existing_product.name = item.name
                existing_product.brand = Brand.objects.get(id=1)
                existing_product.price = item.price
                existing_product.length = item.length
                existing_product.width = item.width
                existing_product.height = item.height
                existing_product.cranking_amperage = item.cranking_amperage
                existing_product.capacity = item.capacity
                existing_product.polarity = item.polarity
                existing_product.voltage = item.voltage

                existing_product.save()
                updated_count += 1

                if item.photo_url and not existing_product.photo:
                    existing_product.photo = save_photo_from_url(item.photo_url)
                    existing_product.save()
                    photos_loaded_count += 1

            else:
                product = Product(
                    art_code=item.art_code,
                    # item.category,
                    # item.good_type,
                    name=item.name,
                    brand=Brand.objects.get(id=1),
                    price=item.price,
                    length=item.length,
                    width=item.width,
                    height=item.height,
                    cranking_amperage=item.cranking_amperage,
                    capacity=item.capacity,
                    polarity=item.polarity,
                    voltage=item.voltage)
                product.save()
                added_count += 1

                if item.photo_url:
                    product.photo = save_photo_from_url(item.photo_url)
                    product.save()
                    photos_loaded_count += 1

        feed_codes_list = [product.art_code for product in products_from_feed]
        base_codes_list = list(Product.objects.filter(in_stock=True).values_list('art_code', flat=True))
        missing_codes = set(base_codes_list) - set(feed_codes_list)
        count_hidden_goods = len(missing_codes) or 0
        Product.objects.filter(art_code__in=missing_codes).update(in_stock=False)

        return updated_count, photos_loaded_count, added_count, count_hidden_goods
