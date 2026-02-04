from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, **extra_fields):

        if not email:
            raise ValueError(_('User must have an email address.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password, **extra_fields):

        must_be_true_fields = ['is_staff', 'is_active', 'is_superuser', 'email_verified']

        for field in must_be_true_fields:
            extra_fields.setdefault(field, True)

            if not extra_fields.get(field):
                raise ValueError(_(f'Superuser must have {field}=True.'))

        extra_fields.setdefault('role', User.ADMIN_ROLE)

        if extra_fields.get('role') != User.ADMIN_ROLE:
            raise ValueError(_('Superuser must have role=admin.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'

    ROLE_CHOICES = (
        (USER_ROLE, _('User')),
        (ADMIN_ROLE, _('Admin')),
    )

    objects = UserManager()

    username = None
    last_name = None
    first_name = None

    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=128, blank=True, db_default='')

    # Better-Auth core fields

    name = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    image = models.TextField(validators=[URLValidator()], blank=True, null=True, default=None)

    # Better-Auth admin() plugin fields
    ban_reason = models.TextField(blank=True, null=True, default=None)
    role = models.TextField(choices=ROLE_CHOICES, db_default=USER_ROLE, blank=True)
    banned = models.BooleanField(db_default=False, blank=True, null=True, default=False)
    ban_expires = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="The date when the user's ban will expire.",
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def get_full_name(self) -> str:
        return self.name


class Address(models.Model):

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    pin_code = models.DecimalField(max_digits=12, decimal_places=0)

    primary = models.BooleanField(default=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='addresses')

    def __str__(self) -> str:
        return f'{self.street_address}, {self.city}, {self.state} - {self.pin_code}'


# The models below are for BetterAuth.
# They don't conform to the snake_case naming convention. Oh, well.


class BetterAuthSession(models.Model):

    token = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, db_column='userId')

    expiresAt = models.DateTimeField()
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    userAgent = models.TextField(blank=True, null=True, default=None)
    ipAddress = models.TextField(blank=True, null=True, default=None)
    # Don't use models.GenericIPAddressField - brighter minds than you have tried and failed.

    # Admin plugin fields
    impersonatedBy = models.TextField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'better_auth_session'


class BetterAuthAccount(models.Model):

    accountId = models.TextField()
    providerId = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, db_column='userId')

    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    scope = models.TextField(blank=True, null=True, default=None)
    password = models.TextField(blank=True, null=True, default=None)

    idToken = models.TextField(blank=True, null=True, default=None)
    accessToken = models.TextField(blank=True, null=True, default=None)
    refreshToken = models.TextField(blank=True, null=True, default=None)

    accessTokenExpiresAt = models.DateTimeField(blank=True, null=True, default=None)
    refreshTokenExpiresAt = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'better_auth_account'


class BetterAuthVerification(models.Model):

    value = models.TextField()
    identifier = models.TextField()

    expiresAt = models.DateTimeField()
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'better_auth_verification'


class BetterAuthJWK(models.Model):

    publicKey = models.TextField()
    privateKey = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    expiresAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'better_auth_jwk'
