from rest_framework import status

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


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
