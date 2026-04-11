from django.db import models
from django.urls import reverse

from backend.utils import generate_slug
from ordered_model.models import OrderedModel
from apps.seller.states import CITIES_CHOICES, STATES_CHOICES


class Seller(models.Model):

    name = models.CharField(max_length=510)
    description = models.TextField(db_default='', blank=True)
    slug = models.SlugField(max_length=510, unique=True, blank=True)

    state = models.CharField(max_length=255, choices=STATES_CHOICES)
    city = models.CharField(max_length=255, choices=CITIES_CHOICES, null=True, blank=True, db_default=None)

    added_on = models.DateTimeField(auto_now_add=True)
    managed_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sellers')

    def get_absolute_url(self) -> str:
        return reverse('api:seller:retrieve', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class SellerPageText(OrderedModel):
    """
    Used to generate dynamic content sections on a seller's page.
    """

    content = models.TextField()
    title = models.CharField(max_length=255)

    image = models.ImageField(upload_to='seller_page_images/', null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='texts')

    order_with_respect_to = 'seller'

    def __str__(self) -> str:
        return self.title
