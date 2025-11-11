from django.urls import path
from rest_framework import DefaultRouter
from . import views
from .views import CreateUserView

router = DefaultRouter()
router.register(r'items', CreateUserView)
urlpatterns = [
    path('api/', include(router.urls)),
    path("schedules/", views.ScheduleListCreate.as_view(), name="schedule-list"),
    path("schedules/delete/<int:pk>/", views.ScheduleDelete.as_view(), name="delete-schedule"),
    path("schedules/generate/", views.GenerateSchedule.as_view(), name="generate-schedule"),
    path("metra/stations/<str:route_id>/", views.GetStations.as_view(), name="metra-stations"),
]