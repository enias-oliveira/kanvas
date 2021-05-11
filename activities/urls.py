from django.urls import path
from .views import ActivityView, StaffActivityView

urlpatterns = [
    path("activities/", ActivityView.as_view()),
    path("activities/<int:user_id>/", StaffActivityView.as_view()),
]
