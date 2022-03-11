from django.contrib import admin
from authentication.models import User
from epicevent.models import Client, Event, Contract
from django.urls import reverse
from django.utils.html import format_html
from datetime import datetime
from django.utils.http import urlencode
from django.utils import timezone


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "last_name", "first_name")
    search_fields = ("username__startswith", "last_name__startswith",)


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ("company_name", "last_name", "first_name", "email", "phone", "sales_contact_id", "view_coming_event_link")
    search_fields = ("company_name__startswith", "last_name__startswith",)

    def view_coming_event_link(self, obj):
        today = datetime.now(tz=timezone.utc)
        coming_event = Event.objects.filter(client_id=obj).filter(event_date__gte=today)
        count = coming_event.count()
        events = list(coming_event.values_list('id', flat=True))
        print(urlencode({"id": events}, True))
        print(events)
        url = (reverse("admin:epicevent_event_changelist")
               + "?"
               + urlencode({"id": events}, True)
               )
        if not coming_event:
            return "No"
        return format_html('<a href="{}">{} Event(s)</a>', url, count)

    view_coming_event_link.short_description = "Coming Event"


@admin.register(Event)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "client_id", "event_date", "support_contact", "view_client_link", "view_contract_link")
    search_fields = ("client_id__company_name__startswith",)

    def view_contract_link(self, obj):
        url = (reverse("admin:epicevent_contract_changelist")
               + str(obj.contract_id.id)
               )
        contract = obj.contract_id
        return format_html('<a href="{}">{} </a>', url, contract)

    view_contract_link.short_description = "Contract"

    def view_client_link(self, obj):
        url = (reverse("admin:epicevent_client_changelist")
               + str(obj.client_id.id)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"


@admin.register(Contract)
class UserAdmin(admin.ModelAdmin):
    list_display = ("client_id", "id", "status", "signed", "sales_contact_id", "view_client_link")
    search_fields = ("client_id__company_name__startswith",)

    def view_client_link(self, obj):
        url = (reverse("admin:epicevent_client_changelist")
               + str(obj.client_id.id)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"

