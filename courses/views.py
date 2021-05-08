from django.contrib.auth.models import User

from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course

from .permissions import CoursePermission

from .serializers import CourseSerializer, CourseRegistrationSerializer


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CoursePermission]

    def get(self, request):
        courses = Course.objects.all()
        serialized_courses = [CourseSerializer(course).data for course in courses]

        return Response(serialized_courses, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_request = CourseSerializer(data=request.data)

        if not serialized_request.is_valid():
            return Response(
                serialized_request.errors, status=status.HTTP_400_BAD_REQUEST
            )

        course = Course.objects.create(**serialized_request.data)

        serialized_course = CourseSerializer(course)

        return Response(serialized_course.data, status=status.HTTP_201_CREATED)


class CourseRegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CoursePermission]

    def put(self, request):
        serialized_request = CourseRegistrationSerializer(data=request.data)

        if not serialized_request.is_valid():
            return Response(
                serialized_request.errors, status=status.HTTP_400_BAD_REQUEST
            )

        course = Course.objects.get(id=serialized_request.data["course_id"])
        course.user_set.set(serialized_request.data["user_ids"])

        serialized_course = CourseSerializer(course)

        return Response(serialized_course.data, status=status.HTTP_200_OK)
