from django.urls import path
from . import views

urlpatterns = [
    path("schedules/", views.ScheduleListCreate.as_view(), name="schedule-list"),
    path("schedules/delete/<int:pk>/", views.ScheduleDelete.as_view(), name="delete-schedule")
]