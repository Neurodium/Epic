from django.db import models
from authentication.models import User

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    sales_contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_sales_contact',
                                         blank=True, null=True)

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    status = models.BooleanField(default=True)
    amount = models.FloatField(max_length=25)
    payment_due = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    sales_contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contract_sales_contact')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contract_client')


class Event(models.Model):
    attendees = models.IntegerField
    event_date = models.DateTimeField
    notes = models.CharField(max_length=35000, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_support_contact')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='event_client')

