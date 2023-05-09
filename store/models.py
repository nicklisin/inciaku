from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    phone = models.EmailField(max_length=200, null=True, default='')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'series'

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'technologies'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=False, default=None)
    type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, default=None)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)
    technology = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='product/', default='', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def photoURL(self):
        try:
            url = self.photo.url
        except (Exception,):
            url = ''
        return url


class DeliveryType(models.Model):
    code = models.TextField(max_length=50, null=True, blank=True)
    name = models.TextField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    code = models.TextField(max_length=50, null=True, blank=True)
    name = models.TextField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.SET_NULL, blank=True, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.get_total for item in orderitems])

    get_cart_total.fget.short_description = 'Total'

    @property
    def get_cart_count(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

    @property
    def get_address(self):
        return ShippingAddress.objects.get(order=self)

    get_address.fget.short_description = 'address'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.SmallIntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product.brand) + '' + str(self.product.name)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address


class PageCategory(models.Model):
    name = models.CharField(max_length=200, null=False)
    url = models.SlugField(allow_unicode=False, null=False, default='', unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=300, null=False)
    title = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=600, null=True)
    body = models.TextField(null=True)
    category = models.ForeignKey(PageCategory, on_delete=models.CASCADE)
    url = models.SlugField(allow_unicode=False, null=False, unique=True)
    order = models.IntegerField(null=False, default=1)
    in_main_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        max_page = Page.objects.order_by('-order').first()
        if max_page and self._state.adding:
            max_value = int(max_page.order) + 10
            self.order = max_value
        super().save(*args, **kwargs)


