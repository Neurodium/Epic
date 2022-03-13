from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contract, Client
from authentication.models import User


# Create your views here.
@login_required
def contract_list(request, client_id):
    client = Client.objects.get(id=client_id)
    contracts = Contract.objects.filter(client_id=client)
    return JsonResponse({'data': [{'id': contract.id, 'name': contract.client_id.company_name + '_' + str(contract.id)} for contract in contracts]})


@login_required
def sales_contact_list(request, client_id):
    client = Client.objects.get(id=client_id)
    sales = User.objects.filter(username=client.sales_contact_id)
    return JsonResponse({'data': [{'id': sale.id, 'name': sale.username} for sale in sales]})
