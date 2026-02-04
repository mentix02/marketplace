from django.db import models


class CartItem(models.Model):

    quantity = models.PositiveSmallIntegerField(db_default=1, default=1, blank=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='+')
