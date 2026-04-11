import uuid

from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField

from backend.utils import generate_slug


class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(db_default='', blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='INR')
    slug = models.SlugField(max_length=settings.DEFAULT_SLUG_SIZE, unique=True, blank=True)

    added_on = models.DateTimeField(auto_now_add=True)
    skey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE, related_name='products')
    primary_image = models.OneToOneField(
        'product.ProductImage', on_delete=models.SET_NULL, null=True, related_name='+', db_default=None, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):

    image = models.ImageField(upload_to='product_images/')
    caption = models.CharField(max_length=255, db_default='', blank=True)
    alt = models.CharField(max_length=255, db_default='', default='', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.caption if self.caption else str(self.id)
