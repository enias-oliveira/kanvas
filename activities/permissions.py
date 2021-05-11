from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException


class ActivityPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_staff:
            raise OnlyStudentCreateActivity

        if request.method == "PUT" and not request.user.is_staff:
            raise OnlyStaffGradeActivity

        return True


class OnlyStudentCreateActivity(APIException):
    status_code = 401
    default_detail = "Only Students can create activities."


class OnlyStaffGradeActivity(APIException):
    status_code = 401
    default_detail = "Only Facilitators or Instructors can grade activities."
