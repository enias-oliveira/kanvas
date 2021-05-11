from rest_framework import serializers, status

from authentication.serializers import UserSerializer

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    repo = serializers.CharField()
    grade = serializers.IntegerField(
        read_only=True, required=False, default=None, allow_null=True
    )

    class Meta:
        model = Activity
        fields = ["id", "user_id", "repo", "grade"]


class ActivityGradeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    grade = serializers.IntegerField()

    def validate_id(self, value):
        if not Activity.objects.filter(id=value).exists():
            raise serializers.ValidationError(detail="Not Found", code=404)
        return value
