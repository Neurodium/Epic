from django.db import models
from django.contrib.auth.models import AbstractUser, Group


from .managers import MyAccountManager

# Create your models here.
class User(AbstractUser):
    MANAGER = 'MANAGER'
    SALES = 'SALES'
    SUPPORT = 'SUPPORT'

    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (SALES, 'Sales'),
        (SUPPORT, 'Support'),
    )

    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=60, unique=True, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='groups', blank=True)

    objects = MyAccountManager()

    def __str__(self):
        return self.username


