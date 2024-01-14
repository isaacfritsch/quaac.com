"""
Database models.
"""
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin)
from django.db import models
from django.core.validators import RegexValidator



class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, name=None, **extra_fields):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError('The Email field must be set')

        if not name:
            raise ValueError('The Name field must be set')

        user = self.model(email=self.normalize_email(email), name=name, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name):
        """Create and return a new superuser."""
        user = self.create_user(email, password, name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    alphanumeric_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]*$',
        message='Apenas letras são permitidas no campo Name.'
    )
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, validators=[alphanumeric_validator])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    
    REQUIRED_FIELDS = ["name"]

    USERNAME_FIELD = 'email'