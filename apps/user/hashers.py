from django.contrib.auth.hashers import Argon2PasswordHasher as BasePasswordHasher


class Argon2PasswordHasher(BasePasswordHasher):
    """
    Custom Argon2 password hasher to match Bun's limit of 1 parallelism.
    """

    time_cost = 2
    parallelism = 1
