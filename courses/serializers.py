from django.contrib.auth.models import User

from rest_framework import serializers

from authentication.serializers import UserSerializer


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    user_set = UserSerializer(read_only=True, many=True)


class CourseRegistrationSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_user_ids(self, value):
        for id in value:
            if not User.objects.filter(id=id).exists():
                raise serializers.ValidationError()
        return value
