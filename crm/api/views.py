from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group
from .pagination import PaginationHandlerMixin
from authentication.models import User
from epicevent.models import Client, Event, Contract
from authentication.permissions import IsSales, IsSupport, IsManager
from .serializers import \
    CreateUserSerializer, UserDetailSerializer, ModifyUserSerializer, UserListSerializer, \
    ClientDetailSerializer, ClientListSerializer, \
    ContractListSerializer, ContractDetailSerializer, \
    EventListSerializer, EventDetailSerializer
import ast
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class LoginUser(APIView):
    """
        Endpoint to log in the application and get the token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data['username']
        try:
            user = User.objects.get(username=username)
        except BaseException as error:
            raise ValidationError({"400": f'{str(error)}'})

        if user.is_active:
            token = RefreshToken.for_user(user)
            response = {"username": username,
                        "token": str(token),
                        "access": str(token.access_token), }
            return Response(response, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"400": f'{user.last_name} {user.first_name} is not active'})
        
        
class UsersViewSet(ModelViewSet):
    """
        This viewset will manage the User model
        - get the list of users
        - get the details of a user
        - create a user
        - update a user
        - delete a user
    """
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    modify_serializer_class = ModifyUserSerializer
    create_serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_serializer_class(self):
        """
            select the correct serializer class depending on the action called
        """
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'update':
            return self.modify_serializer_class
        elif self.action == 'create':
            return self.create_serializer_class
        else:
            return super().get_serializer_class()

    def create(self, request):
        """
            custom creation to insert a list of groups
        """
        serializer = CreateUserSerializer(data=request.data)
        groups = ast.literal_eval(request.data['groups'])
        if serializer.is_valid():
            serializer.save(groups=groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username=None):
        """
            custom update to insert a list of groups
        """
        user = User.objects.get(username=username)
        serializer = ModifyUserSerializer(user, data=request.data)
        groups = ast.literal_eval(request.data['groups'])
        if serializer.is_valid():
            serializer.save(groups=groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        """
            generates custom message when deletes the user
        """
        user = User.objects.get(username=username)
        user.delete()
        return Response(f"{user.username} has been deleted", status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(ModelViewSet):
    """
        Viewset to manage Client model
        - get the list of clients
        - retrieve the details of a user
        - create a client
        - update a client
    """
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    queryset = Client.objects.all()
    lookup_field = 'company_name'

    def get_serializer_class(self):
        """
            get the list serializer when using the action 'list'
            get the detail serializer for all other actions
        """
        if self.action == 'list':
            return super().get_serializer_class()
        else:
            return self.detail_serializer_class

    def get_permissions(self):
        """
            Check the permission by action
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsSales | IsManager]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsSales]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """
            check if client sales contact is from sales group before creating a client
        """
        serializer = ClientDetailSerializer(data=request.data)
        sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if sales_contact.groups.filter(name='sales').exists():
            if serializer.is_valid():
                serializer.save(sales_contact_id=sales_contact)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"{sales_contact} is not from sales team")

    def update(self, request, company_name=None):
        """
            check if client sales contact is from sales group before updating a client
            check if current user is sales contact assigned to the client
        """
        client = Client.objects.get(company_name=company_name)
        serializer = ClientDetailSerializer(client, data=request.data)
        if request.data['sales_contact_id']:
            sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if request.user.groups.filter(name='manager').exists() or request.user == client.sales_contact_id:
            if serializer.is_valid():
                if request.data['sales_contact_id']:
                    if sales_contact.groups.filter(name='sales').exists():
                        serializer.save(sales_contact_id=sales_contact)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(f"{sales_contact} is not from sales team")
                serializer.save(sales_contact_id=None)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You do not have permission to update {client}")




class ContractViewSet(ModelViewSet):
    """
        Viewset to manage Contract model:
        - get list of contracts
        - retrieve details of a contract
        - create a contract
        - update a contract
    """
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        """
            get the list serializer when using the action 'list'
            get the detail serializer for all other actions
        """
        if self.action == 'list':
            return super().get_serializer_class()
        else:
            return self.detail_serializer_class

    def get_permissions(self):
        """
            Check the permission by action
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsSales | IsManager]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsSales]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """
            checks if sales contact in the contract is the same as the client before creating the object
        """
        serializer = ContractDetailSerializer(data=request.data)
        client = Client.objects.get(company_name=request.data['client_id'])
        if serializer.is_valid():
            serializer.save(client_id=client, sales_contact_id=client.sales_contact_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, id=None):
        """
            checks if current user is the sales contact assigned to the client
            checks if sales contact in the contract is the same assigned to client before updating the object
        """
        contract = Contract.objects.get(id=id)
        serializer = ContractDetailSerializer(contract, data=request.data)
        client = Client.objects.get(company_name=request.data['client_id'])
        sales_contact = User.objects.get(username=client.sales_contact_id)
        if request.user.groups.filter(name='manager').exists() or request.user == contract.sales_contact_id:
            if serializer.is_valid():
                serializer.save(client_id=client, sales_contact_id=sales_contact)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You do not have rights to update contract {client.company_name}_{contract.id}"
                        f" of {client.company_name}")


class EventViewSet(ModelViewSet):
    """
        Viewset to manage Event model:
        - get list of events
        - retrieve details of an event
        - create an event
        - update an event
    """
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        """
            get the list serializer when using the action 'list'
            get the detail serializer for all other actions
        """
        if self.action == 'list':
            return super().get_serializer_class()
        else:
            return self.detail_serializer_class

    def get_permissions(self):
        """
            Check the permission by action
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsSales | IsManager | IsSupport]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsSales]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request): 
        """
            checks if a support contract has been submitted, and if yes, support contact has to be part of group support
            checks if the contract is active (signed) 
        """
        data = request.data
        serializer = EventDetailSerializer(data=data)
        client = Client.objects.get(company_name=data['client_id'])
        contract = Contract.objects.get(id=data['contract_id'])
        if data['support_contact']:
            support_contact = User.objects.get(username=data['support_contact'])
        event = Event.objects.filter(contract_id=contract)
        if not event:
            if contract.client_id == client:
                if contract.status is True:
                    if serializer.is_valid():
                        if data['support_contact']:
                            if support_contact.groups.filter(name='support').exists():
                                serializer.save(client_id=client, support_contact=support_contact, contract_id=contract)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            return Response(f"{support_contact} is not from support team")
                        serializer.save(client_id=client, contract_id=contract)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response("Contract is not signed")
            return Response(f"{client.company_name} sales contact is {client.sales_contact_id}")
        return Response("Contract is already used")


    def update(self, request, id=None):
        """
            checks if a support contract has been submitted, and if yes, support contact has to be part of group support
            checks if the contract is active (signed) 
            checks if current user is sales contact or support contact assigned
        """
        data = request.data
        event = Event.objects.get(id=id)
        serializer = EventDetailSerializer(event, data=request.data)
        client = Client.objects.get(company_name=event.client_id)
        contract = Contract.objects.get(id=event.contract_id.id)
        if data['support_contact']:
            new_support_contact = User.objects.get(username=data['support_contact'])
        if request.user.groups.filter(name='manager').exists() \
                or request.user == client.sales_contact_id \
                or request.user == event.support_contact:
            if contract.client_id == client:
                if contract.status is True:
                    if serializer.is_valid():
                        if data['support_contact']:
                            if new_support_contact.groups.filter(name='support').exists():
                                serializer.save(client_id=client,
                                                support_contact=new_support_contact,
                                                contract_id=contract)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            return Response(f"{new_support_contact} is not from support team")
                        serializer.save(client_id=client,
                                        support_contact=None,
                                        contract_id=contract)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response("Contract is not signed")
            return Response(f"{client.company_name} sales contact is {client.sales_contact_id}")
        return Response("You do not have rights to update this event")


class ComingEventViewSet(ModelViewSet):
    """
        returns all the coming events with the list action
        returns the coming events of a client with the retrieve action
    """
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    today = datetime.now(tz=timezone.utc)
    queryset = Event.objects.filter(event_date__gte=today)
    lookup_field = 'client_id'

    def get_serializer_class(self):
        """
            get the list serializer when using the action 'list'
            get the detail serializer for all other actions
        """
        if self.action == 'list':
            return super().get_serializer_class()
        else:
            return self.detail_serializer_class

    def get_permissions(self):
        """
            Check the permission by action
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsSales]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsSales]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, client_id):
        client = get_object_or_404(Client, company_name=client_id)
        events = self.queryset.filter(client_id=client)
        serializer = EventDetailSerializer(events, many=True)
        return Response(serializer.data)


class MissingClientSales(APIView, PaginationHandlerMixin):
    """
        returns all clients which do not have sales contact assigned
    """
    permission_classes = [IsAuthenticated, IsManager]
    pagination_class = BasicPagination

    def get(self, request):
        clients = Client.objects.filter(sales_contact_id__isnull=True)
        if not clients:
            return Response("All clients have a sales contact")
        page = self.paginate_queryset(clients)
        if page is not None:
            serializer = self.get_paginated_response(ClientListSerializer(page, many=True).data)
        else:
            serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MissingEventSupport(APIView, PaginationHandlerMixin):
    """
        returns all events which does not have a support contact
    """
    permission_classes = [IsAuthenticated, IsManager]
    pagination_class = BasicPagination

    def get(self, request):
        events = Event.objects.filter(support_contact__isnull=True)
        if not events:
            return Response("All events have a support contact")
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_paginated_response(EventListSerializer(page, many=True).data)
        else:
            serializer = EventListSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PotentialClients(APIView, PaginationHandlerMixin):
    """
        returns all clients which have not signed a contract
    """
    permission_classes = [IsAuthenticated, IsSales]
    pagination_class = BasicPagination

    def get(self, request):
        contracts = list(Contract.objects.filter(status=True))
        signed_clients = [contract.client_id.id for contract in contracts]
        clients = Client.objects.exclude(id__in=signed_clients)
        if not clients:
            return Response("All clients have signed a contract")
        page = self.paginate_queryset(clients)
        if page is not None:
            serializer = self.get_paginated_response(ClientListSerializer(page, many=True).data)
        else:
            serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupportEvents(APIView, PaginationHandlerMixin):
    """
        returns the list of events assigned to the support contact who makes the request
    """
    permission_classes = [IsAuthenticated, IsSupport]
    pagination_class = BasicPagination

    def get(self, request):
        events = list(Event.objects.filter(support_contact=request.user))
        if not events:
            return Response("You do not have any event assigned to you")
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_paginated_response(EventListSerializer(page, many=True).data)
        else:
            serializer = EventListSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


