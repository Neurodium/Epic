from django.contrib import admin
from authentication.models import User
from epicevent.models import Client, Event, Contract


# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Contract)
