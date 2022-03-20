from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from authentication.models import User
from epicevent.models import Client, Contract, Event


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class CreateUserSerializer(ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'last_name', 'first_name', 'email', 'join_date', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            join_date=validated_data['join_date'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user.groups.set(validated_data['groups'])
        return user


class ModifyUserSerializer(ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'join_date', 'email', 'groups']


class LoginUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserDetailSerializer(ModelSerializer):
    
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'join_date', 'email', 'groups']


class UserInfoSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email']


class ClientDetailSerializer(ModelSerializer):

    sales_contact_id = UserInfoSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'sales_contact_id']


class ClientInfoSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone', 'mobile']


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'company_name', 'first_name', 'last_name', 'email']


class ContractDetailSerializer(ModelSerializer):

    sales_contact_id = UserInfoSerializer(read_only=True)
    client_id = ClientInfoSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = ['status', 'client_id', 'sales_contact_id', 'amount', 'payment_due']


class ContractListSerializer(ModelSerializer):
    client_id = ClientListSerializer(read_only=True)
    sales_contact_id = UserListSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'status', 'client_id', 'sales_contact_id']


class ContractInfoSerializer(ModelSerializer):
    sales_contact_id = UserInfoSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'status', 'sales_contact_id', 'amount', 'payment_due']


class EventListSerializer(ModelSerializer):
    support_contact = UserListSerializer(read_only=True)
    contract_id = ContractListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'contract_id', 'event_date', 'support_contact']


class EventDetailSerializer(ModelSerializer):
    support_contact = UserInfoSerializer(read_only=True)
    contract_id = ContractInfoSerializer(read_only=True)
    client_id = ClientInfoSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['attendees', 'event_date', 'notes', 'client_id', 'support_contact', 'contract_id']
        
