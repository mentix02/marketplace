from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.user.models import User, BetterAuthAccount


BETTER_AUTH_CREDENTIALS_PROVIDER_ID = 'credential'


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_better_auth_account(sender: type[User], instance: User = None, created: bool = False, **kwargs):
    BetterAuthAccount.objects.update_or_create(
        user=instance,
        providerId=BETTER_AUTH_CREDENTIALS_PROVIDER_ID,
        defaults={'accountId': instance.id, 'password': instance.password},
    )
