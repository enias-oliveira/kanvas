from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CredentialSerializer


class AccountView(APIView):
    def post(self, request):
        serialized_request = UserSerializer(data=request.data)

        if not serialized_request.is_valid():
            return Response(status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            username=serialized_request.data["username"],
            password=request.data["password"],
            is_staff=serialized_request.data["is_staff"],
            is_superuser=serialized_request.data["is_superuser"],
        )

        serialized_user = UserSerializer(user)

        return Response(serialized_user.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serialized_request = CredentialSerializer(data=request.data)

        if not serialized_request.is_valid():
            return Response(
                serialized_request.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=request.data["username"],
            password=request.data["password"],
        )
        token = Token.objects.get_or_create(user=user)[0]
        return Response({"token": token.key})
