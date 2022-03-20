from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.permissions import IsSales, IsManager, IsSupport


# Register your models here.
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


class ClientContract(admin.SimpleListFilter):
    """
        Filter to check if a client has a signed contract
        - Yes: There is at least a signed contract
        - No: There is no signed contract
    """
    title = _('signed contract')

    parameter_name = 'signed_contract'

    def lookups(self, request, model_admin):

        return(
            ('Yes', _('has signed a contract')),
            ('No', _('has not signed a contract')),
        )

    def queryset(self, request, queryset):
        contracts = list(Contract.objects.filter(status=True))
        signed_clients = [contract.client_id.id for contract in contracts]

        if self.value() == 'Yes':
            return queryset.filter(id__in=signed_clients)

        if self.value() == 'No':
            return queryset.exclude(id__in=signed_clients)


class SupportEvents(admin.SimpleListFilter):
    """
        Filter to check events by support contact who is making the request
    """
    title = _('my events')

    parameter_name = 'supported_events'

    def lookups(self, request, model_admin):

        return(
            ('MyEvents', _('my events')),
            ('All', _('all events')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'MyEvents':
            return queryset.filter(support_contact=request.user)
        if self.value() == 'All':
            return queryset


class UserCreationAdminForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class UserChangeAdminForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields


class ClientAdminForm(forms.ModelForm):
    """
        filter sales contact to get user only from sales group
    """
    class Meta(object):
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ClientAdminForm, self).__init__(*args, **kwargs)

        users = User.objects.filter(groups__name="sales")
        self.fields['sales_contact_id'] = forms.ModelChoiceField(queryset=users, required=False)


class ContractAdminForm(forms.ModelForm):
    """
        Contract form to create/change contracts objects:
        create a filter to retrieve the sales contact assigned to the client
    """
    class Meta(object):
        model = Contract
        fields = ["status", "client_id", "sales_contact_id", "amount", "payment_due"]

    def __init__(self, *args, **kwargs):
        super(ContractAdminForm, self).__init__(*args, **kwargs)

        try:
            self.initial['client_id'] = kwargs['instance'].client_id.id
        except KeyError:
            pass
        client_list = [('', '---------')] + [(client.id, client) for client in Client.objects.all()]

        try:
            self.initial['sales_id'] = kwargs['instance'].sales_contact_id.id
            sales_init_form = [(sales.id, sales) for sales in
                               User.objects.filter(username=kwargs['instance'].client_id.sales_contact_id
                                                   )]
        except KeyError:
            sales_init_form = [('', '---------')]

        try:
            self.fields['client_id'].widget = forms.Select(attrs={'id': 'id_client',
                                                                  'onchange': 'getSales(this.value)',
                                                                  'style': 'width:200px'
                                                                  },
                                                           choices=client_list,
                                                           )

            self.fields['sales_contact_id'].widget = \
                forms.Select(attrs={'id': 'id_sales',
                                    'style': 'width:200px'
                                    },
                             choices=sales_init_form
                             )

        except KeyError:
            pass


class EventAdminForm(forms.ModelForm):
    """
        form to create events
        create a filter to choose the contract signed and not used in an event
        create a filter to get the support contact with a user from support group
    """
    class Meta(object):
        model = Event
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        contract = cleaned_data['contract_id']
        if contract.status is False:
            raise forms.ValidationError("Contract is not signed")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)

        users = User.objects.filter(groups__name="support")
        self.fields['support_contact'] = forms.ModelChoiceField(queryset=users, required=False)
        try:
            self.initial['client_id'] = kwargs['instance'].client_id.id
        except KeyError:
            pass
        client_list = [('', '---------')] + [(client.id, client) for client in Client.objects.all()]

        try:
            self.initial['contract_id'] = kwargs['instance'].contract_id.id
            contract_init_form = [(contract.id, contract) for contract in Contract.objects.filter(
                client_id=kwargs['instance'].client_id
            )]
        except KeyError:
            contract_init_form = [('', '---------')]

        try:
            self.fields['client_id'].widget = forms.Select(attrs={'id': 'id_client',
                                                                  'onchange': 'getContracts(this.value)',
                                                                  'style': 'width:200px'
                                                                  },
                                                           choices=client_list,
                                                           )

            self.fields['contract_id'].widget = forms.Select(attrs={
                'id': 'id_contract',
                'style': 'width:200px'
                },
                choices=contract_init_form
            )
        except KeyError:
            pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    list_display = ("username", "id", "last_name", "first_name", "email")
    search_fields = ("username__startswith", "last_name__startswith",)

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if (
                not is_superuser
                and obj is not None
        ):
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    fields = ("company_name", "last_name", "first_name", "email", "phone", "mobile", "sales_contact_id")
    list_display = ("company_name", "last_name", "first_name", "email", "phone", "sales_contact_id",
                    "view_coming_event_link")
    search_fields = ("company_name__startswith", "last_name__startswith",)
    list_filter = ("sales_contact_id", ClientContract)

    def has_change_permission(self, request, *obj):
        """
            update is allowed only if user is assigned to manager group
            update is allowed if user is sales assigned to the client
        """
        if obj:
            if obj[0] is not None:
                if request.user == obj[0].sales_contact_id:
                    return True
        if request.user.groups.filter(name='manager').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def view_coming_event_link(self, obj):
        """
            create url to get the list of coming event for a client
        """
        today = datetime.now(tz=timezone.utc)
        coming_event = Event.objects.filter(client_id=obj).filter(event_date__gte=today)
        count = coming_event.count()
        url = (reverse("admin:epicevent_event_changelist")
               + "?"
               + urlencode({"client_id": obj.id}, True)
               + "&agenda=future_events"
               )
        if not coming_event:
            return "No"
        return format_html('<a href="{}">{} Event(s)</a>', url, count)

    view_coming_event_link.short_description = "Coming Event"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ("id", "client_id", "event_date", "support_contact", "view_client_link",
                    "client_phone", "client_email", "view_contract_link", "contract_sales")
    search_fields = ("client_id__company_name__startswith",)
    list_filter = ("client_id__company_name", ComingEvent, SupportEvents)

    class Media:
        js = (
            'js/chained-area.js',
        )

    def has_change_permission(self, request, *obj):
        """
            update is allowed only if user is assigned to manager group
            update is allowed if user is sales assigned to the client
            update is allowed if user is support assigned to the event
        """
        if obj:
            if obj[0] is not None:
                if request.user == obj[0].client_id.sales_contact_id:
                    return True
        if obj:
            if obj[0] is not None:
                if request.user == obj[0].support_contact:
                    return True
        if request.user.groups.filter(name='manager').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def view_contract_link(self, obj):
        """
            create the url to view the contract object
        """
        url = (reverse("admin:epicevent_contract_changelist")
               + "?"
               + urlencode({"id": obj.contract_id.id}, True)
               )
        contract = obj.contract_id
        return format_html('<a href="{}">{} </a>', url, contract)

    view_contract_link.short_description = "Contract"

    def contract_sales(self, obj):
        """
            display the sales contact of the contract
        """
        contract = Contract.objects.get(id=obj.contract_id.id)
        return contract.sales_contact_id

    contract_sales.short_description = "Sales Contact"

    def view_client_link(self, obj):
        """
            create the url to view the clients details
        """
        url = (reverse("admin:epicevent_client_changelist")
               + "?"
               + urlencode({"id": obj.client_id.id}, True)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"

    def client_phone(self, obj):
        """
            get the client phone
        """
        client = obj.client_id
        return client.phone

    client_phone.short_description = "Phone"

    def client_email(self, obj):
        """
            get the client email
        """
        client = obj.client_id
        return client.email

    client_email.short_description = "Email"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    form = ContractAdminForm
    list_display = ("id", "view_client_link", "status", "sales_contact_id", "related_event")
    search_fields = ("client_id__company_name__startswith",)
    list_filter = ("client_id__company_name", "sales_contact_id")

    class Media:
        js = (
            'js/chained-area.js',
        )

    def has_change_permission(self, request, *obj):
        """
            update is allowed only if user is assigned to manager group
            update is allowed if user is sales assigned to the client
        """
        if obj:
            if obj[0] is not None:
                if request.user == obj[0].sales_contact_id:
                    return True
        if request.user.groups.filter(name='manager').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def view_client_link(self, obj):
        """
            create url to view client details
        """
        url = (reverse("admin:epicevent_client_changelist")
               + "?"
               + urlencode({"id": obj.client_id.id}, True)
               )
        client = obj.client_id
        return format_html('<a href="{}">{} </a>', url, client)

    view_client_link.short_description = "Client"

    def related_event(self, obj):
        """
            show the event related to the contract
        """
        event = Event.objects.get(contract_id=obj.id)
        url = (reverse("admin:epicevent_event_changelist")
               + "?"
               + urlencode({"id": event.id}, True)
               )
        return format_html('<a href="{}">{} </a>', url, event)
