from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.models import Group
from .pagination import PaginationHandlerMixin
from authentication.models import User
from epicevent.models import Client, Event, Contract
from authentication.permissions import IsSales, IsSupport, IsManager
from .serializers import CreateUserSerializer, UserDetailSerializer, ModifyUserSerializer, UserListSerializer, \
    ClientDetailSerializer, ClientListSerializer
import ast



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


class UserManagement(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_user(username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        user = self.get_user(username)
        data = request.data
        serializer = ModifyUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = self.get_user(username)
        user.delete()
        return Response(f"{user.username} has been deleted", status=status.HTTP_204_NO_CONTENT)


class UserList(UserManagement, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsManager]
    pagination_class = BasicPagination

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        groups = ast.literal_eval(request.data['groups'])
        if serializer.is_valid():
            serializer.save(groups=groups)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_paginated_response(UserListSerializer(page, many=True).data)
        else:
            serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, IsSales | IsManager | IsSupport]

    def get_client(self, client_id):
        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, client_id):
        client = self.get_client(client_id)
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, client_id):
        client = self.get_client(client_id)
        data = request.data
        serializer = ModifyUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientList(ClientView):
    permission_classes = [IsAuthenticated, IsSales | IsManager | IsSupport]
    pagination_class = BasicPagination

    def get(self, request):
        clients = Client.objects.all()
        page = self.paginate_queryset(clients)
        if page is not None:
            serializer = self.get_paginated_response(ClientListSerializer(page, many=True).data)
        else:
            serializer = ClientListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)