from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contract, Client, Event
from authentication.models import User


# Create your views here.
@login_required
def contract_list(request, client_id):
    """
        This view returns the list of contract linked to a client and not used in an event
        This view will be used in the admin interface to filter the list of contracts in the Event form
    """
    client = Client.objects.get(id=client_id)
    events = list(Event.objects.filter(client_id=client))
    contract_used = [event.contract_id.id for event in events]
    contracts = Contract.objects.filter(client_id=client).filter(status=True).exclude(id__in=contract_used)
    return JsonResponse({'data': [{'id': contract.id, 'name': contract.client_id.company_name + '_' + str(contract.id)} 
                                  for contract in contracts]})


@login_required
def sales_contact_list(request, client_id):
    """
        This view returns the sale contact of a client
        This view will be used to get the sale contact when creating a contract
    """
    client = Client.objects.get(id=client_id)
    sales = User.objects.filter(username=client.sales_contact_id)
    return JsonResponse({'data': [{'id': sale.id, 'name': sale.username} for sale in sales]})
