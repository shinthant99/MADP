from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomerManagement(BaseUserManager):
    """Manges customerprofiles"""
    def create_customer(self, phone, email, name, password=None):
        if not email:
            raise ValueError("You need an email address to make an account.")
        email = self.normalize_email(email)
        user=self.model(phone=phone, email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superman(self, phone, email, name, password):
        user = self.create_customer(phone, email, name, password)
        user.is_superuser = True
        user.staff_status = True
        user.save(using=self._db)
        return user

    
# Create your models here.
class CustomerProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for customers"""
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255, unique=True)
    customer_phone = models.IntegerField(null=False, blank=False, unique=True)
    account_activated = models.BooleanField(default=True)
    staff_status = models.BooleanField(default=False)

    objects = CustomerManagement()
    USERNAME_FIELD = 'customer_phone'
    REQUIRED_FIELDS = ['email']

    def get_name(self):
        return self.customer_name

    def get_phone(self):
        return self.customer_phone
    
    def get_email(self):
        return self.customer_email

    def __str__(self):
        return self.name
    
