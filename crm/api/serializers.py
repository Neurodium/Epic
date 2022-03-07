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
        fields = ['username', 'password', 'role', 'last_name', 'first_name', 'join_date', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            join_date=validated_data['join_date'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user.groups.set(validated_data['groups'])
        return user


class ModifyUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['role', 'last_name', 'first_name', 'join_date']


class LoginUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class UserDetailSerializer(ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'role', 'last_name', 'first_name', 'join_date', 'is_staff', 'creation_date',
                  'update_date', 'groups']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'



class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'company_name', 'first_name', 'last_name']


class ModifyClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['company_name', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'sales_contact_id']
