from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CreateUserView


urlpatterns = [
    # path('api/', views.CreateUserView.as_view()),
    path("schedules/", views.ScheduleListCreate.as_view(), name="schedule-list"),
    path("schedules/delete/<int:pk>/", views.ScheduleDelete.as_view(), name="delete-schedule"),
    path("schedules/generate/", views.GenerateSchedule.as_view(), name="generate-schedule"),
    path("metra/stations/<str:route_id>/", views.GetStations.as_view(), name="metra-stations"),
    path('matches/', views.GetStudentMatches.as_view(), name='student_matches'),
]