from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course

from .permissions import CoursePermission

from .serializers import CourseSerializer


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CoursePermission]

    def post(self, request):
        serialized_request = CourseSerializer(data=request.data)

        if not serialized_request.is_valid():
            return Response(
                serialized_request.errors, status=status.HTTP_400_BAD_REQUEST
            )

        course = Course.objects.create(**serialized_request.data)

        serialized_course = CourseSerializer(course)

        return Response(serialized_course.data, status=status.HTTP_201_CREATED)
