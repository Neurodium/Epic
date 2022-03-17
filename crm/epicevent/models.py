from django.db import models
from authentication.models import User

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=250, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    sales_contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_sales_contact',
                                         blank=True, null=True)

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    status = models.BooleanField(default=False)
    amount = models.FloatField(max_length=25)
    payment_due = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    sales_contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contract_sales_contact')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contract_client')
    
    def __str__(self):
        return self.client_id.company_name + "_" + str(self.id)


class Event(models.Model):
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.CharField(max_length=35000, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    support_contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_support_contact',
                                        blank=True, null=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='event_client')
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='event_contract')
    
    class Meta:
        unique_together = ['client_id', 'contract_id']

    def __str__(self):
        return self.client_id.company_name + "_" + str(self.contract_id.id) + "_" + str(self.event_date)

