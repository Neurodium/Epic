from django.contrib import admin
from authentication.models import User
from epicevent.models import Client, Event, Contract
from django.urls import reverse
from django.utils.html import format_html
from datetime import datetime
from django.utils.http import urlencode
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import *
from django import forms


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "last_name", "first_name")
    search_fields = ("username__startswith", "last_name__startswith",)


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ("company_name", "last_name", "first_name", "email", "phone", "sales_contact_id",
                    "view_coming_event_link")
    search_fields = ("company_name__startswith", "last_name__startswith",)

    def view_coming_event_link(self, obj):
        today = datetime.now(tz=timezone.utc)
        coming_event = Event.objects.filter(client_id=obj).filter(event_date__gte=today)
        count = coming_event.count()
        events = list(coming_event.values_list('id', flat=True))
        url = (reverse("admin:epicevent_event_changelist")
               + "?"
               + urlencode({"client_id": obj.id}, True)
               + "&agenda=future_events"
               )
        if not coming_event:
            return "No"
        return format_html('<a href="{}">{} Event(s)</a>', url, count)

    view_coming_event_link.short_description = "Coming Event"


class ComingEvent(admin.SimpleListFilter):
    """ Filter used to select only icoming events:
    values:
        - less than a month: events booked between today and in a month
        - in the next 3 months: events booked between today and in 3 months
        - all coming events: all events that are coming
    """
    title = _('coming event')

    parameter_name = 'agenda'

    def lookups(self, request, model_admin):

        return(
            ('<1M', _('less than a month')),
            ('<3M', _('in the next 3 months')),
            ('future_events', _('all coming events')),
        )

    def queryset(self, request, queryset):
        today = datetime.now(tz=timezone.utc)
        one_month = today + relativedelta(months=+1)
        three_months = today + relativedelta(months=+3)

        if self.value() == '<1M':
            return queryset.filter(event_date__gte=today,
                                   event_date__lte=one_month)

        if self.value() == '<3M':
            return queryset.filter(event_date__gte=today,
                                   event_date__lte=three_months)

        if self.value() == 'future_events':
            return queryset.filter(event_date__gte=today)


@admin.register(Event)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "client_id", "event_date", "support_contact", "view_client_link",
                    "client_phone", "client_email", "view_contract_link", "contract_sales")
    search_fields = ("client_id__company_name__startswith",)
    list_filter = ("client_id__company_name", ComingEvent)

    def view_contract_link(self, obj):
        url = (reverse("admin:epicevent_contract_changelist")
               + "?"
               + urlencode({"id": obj.contract_id.id}, True)
               )
        contract = obj.contract_id
        return format_html('<a href="{}">{} </a>', url, contract)

    view_contract_link.short_description = "Contract"

    def contract_sales(self, obj):
        contract = Contract.objects.get(id=obj.contract_id.id)
        return contract.sales_contact_id

    contract_sales.short_description = "Sales Contact"

    def view_client_link(self, obj):
        url = (reverse("admin:epicevent_client_changelist")
               + "?"
               + urlencode({"id": obj.client_id.id}, True)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"

    def client_phone(self, obj):
        client = obj.client_id
        return client.phone

    client_phone.short_description = "Phone"

    def client_email(self, obj):
        client = obj.client_id
        return client.email

    client_email.short_description = "Email"


@admin.register(Contract)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "view_client_link", "status", "signed", "sales_contact_id", "related_event")
    search_fields = ("client_id__company_name__startswith",)
    list_filter = ("client_id__company_name",)

    def view_client_link(self, obj):
        url = (reverse("admin:epicevent_client_changelist")
               + "?"
               + urlencode({"id": obj.client_id.id}, True)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"

    def related_event(self, obj):
        event = Event.objects.get(contract_id=obj.id)
        url = (reverse("admin:epicevent_event_changelist")
               + "?"
               + urlencode({"id": event.id}, True)
               )
        return format_html('<a href="{}">{} </a>', url, event)


