from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
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
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    modify_serializer_class = ModifyUserSerializer
    create_serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'update':
            return self.modify_serializer_class
        elif self.action == 'create':
            return self.create_serializer_class
        else:
            return super().get_serializer_class()

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        groups = ast.literal_eval(request.data['groups'])
        if serializer.is_valid():
            serializer.save(groups=groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username=None):
        user = User.objects.get(username=username)
        serializer = ModifyUserSerializer(user, data=request.data)
        groups = ast.literal_eval(request.data['groups'])
        if serializer.is_valid():
            serializer.save(groups=groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        user = User.objects.get(username=username)
        user.delete()
        return Response(f"{user.username} has been deleted", status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(ModelViewSet):
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    queryset = Client.objects.all()
    lookup_field = 'company_name'

    def get_serializer_class(self):
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
        serializer = ClientDetailSerializer(data=request.data)
        sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if sales_contact.groups.filter(name='sales').exists():
            if serializer.is_valid():
                serializer.save(sales_contact_id=sales_contact)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"{sales_contact} is not from sales team")

    def update(self, request, company_name=None):
        client = Client.objects.get(company_name=company_name)
        serializer = ClientDetailSerializer(client, data=request.data)
        sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if sales_contact.groups.filter(name='sales').exists():
            if request.user == client.sales_contact_id:
                if serializer.is_valid():
                    serializer.save(sales_contact_id=sales_contact)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(f"You do not have rights to update {client.company_name}")
        return Response(f"{sales_contact} is not from sales team")


class ContractViewSet(ModelViewSet):
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
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
        serializer = ContractDetailSerializer(data=request.data)
        client = Client.objects.get(company_name=request.data['client_id'])
        sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if client.sales_contact_id == sales_contact:
            if serializer.is_valid():
                serializer.save(client_id=client, sales_contact_id=sales_contact)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"{client.company_name} sales contact is {client.sales_contact_id}")

    def update(self, request, id=None):
        contract = Contract.objects.get(id=id)
        serializer = ContractDetailSerializer(contract, data=request.data)
        client = Client.objects.get(company_name=contract.client_id.company_name)
        sales_contact = User.objects.get(username=client.sales_contact_id)
        new_sales_contact = User.objects.get(username=request.data['sales_contact_id'])
        if request.user == sales_contact:
            if client.sales_contact_id == new_sales_contact:
                if serializer.is_valid():
                    serializer.save(client_id=client, sales_contact_id=new_sales_contact)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(f"{client.company_name} sales contact is {client.sales_contact_id}")
        return Response(f"You do not have rights to update contract {client.company_name}_{contract.id}"
                        f" of {client.company_name}")


class EventViewSet(ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
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
        data = request.data
        event = Event.objects.get(id=id)
        serializer = EventDetailSerializer(event, data=request.data)
        client = Client.objects.get(company_name=event.client_id)
        contract = Contract.objects.get(id=event.contract_id.id)
        if event.support_contact:
            support_contact = User.objects.get(username=event.support_contact)
        if data['support_contact']:
            new_support_contact = User.objects.get(username=data['support_contact'])
        if request.user == client.sales_contact_id or event.support_contact:
            if contract.client_id == client:
                if contract.status is True:
                    if new_support_contact.groups.filter(name='support').exists():
                        if serializer.is_valid():
                            if data['support_contact']:
                                serializer.save(client_id=client,
                                                support_contact=new_support_contact,
                                                contract_id=contract)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            serializer.save(client_id=client,
                                            contract_id=contract)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(f"{new_support_contact} is not from support team")
                return Response("Contract is not signed")
            return Response(f"{client.company_name} sales contact is {client.sales_contact_id}")
        return Response("You do not have rights to update this event")