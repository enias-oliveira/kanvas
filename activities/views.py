from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Activity

from .serializers import ActivitySerializer, ActivityGradeSerializer

from .permissions import ActivityPermission


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ActivityPermission]

    def get(self, request):

        if not request.user.is_staff:
            activities = Activity.objects.filter(user_id=request.user.id)
        else:
            activities = Activity.objects.all()

        serialized_activities = ActivitySerializer(activities, many=True)

        return Response(serialized_activities.data)

    def post(self, request):
        serialized_request = ActivitySerializer(data=request.data)

        serialized_request.is_valid(raise_exception=True)

        activity = Activity.objects.get_or_create(
            repo=serialized_request.data["repo"],
            user_id=request.user,
            defaults={**serialized_request.data},
        )[0]

        serialized_activity = ActivitySerializer(activity)

        return Response(
            serialized_activity.data,
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):
        serialized_request = ActivityGradeSerializer(data=request.data)

        try:
            serialized_request.is_valid(raise_exception=True)

            request_activity = Activity.objects.get(id=serialized_request.data["id"])
            request_activity.grade = serialized_request.data["grade"]
            request_activity.save()

            serialized_activity = ActivitySerializer(request_activity)

            return Response(
                serialized_activity.data,
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as Error:
            status_code = (
                status.HTTP_404_NOT_FOUND
                if Error.detail["id"][0].code == 404
                else status.HTTP_400_BAD_REQUEST
            )

            return Response(serialized_request.errors, status=status_code)
