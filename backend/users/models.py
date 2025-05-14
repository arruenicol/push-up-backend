from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Modelo de usuario extendido"""
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)  # Make first_name required
    last_name = models.CharField(_('last name'), max_length=150)    # Make last_name required
    push_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Utilizamos el email como username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Add first_name and last_name to required fields
    
    def __str__(self):
        return self.email