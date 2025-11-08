from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, ScheduleSerializer
from .models import Schedule

# from .forms import UploadForm
from .utils import parse_ics

class ScheduleListCreate(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Schedule.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            count = Schedule.objects.filter(author=user).count()
            title = f"schedule_{count + 1}"

            serializer.save(author=user, title=title)
        else:
            print(serializer.errors)

class ScheduleDelete(generics.DestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Schedule.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class GenerateSchedule(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Get the latest uploaded schedule
        schedule = Schedule.objects.filter(author=user).order_by('-uploaded_at').first()
        if not schedule:
            return Response({"error": "No schedule uploaded"}, status=400)

        # Parse ICS → Python objects
        try:
            events = parse_ics(schedule.file.path)
        except Exception as e:
            return Response(
                {"error": f"Failed to parse schedule: {e}"},
                status=500
            )

        # TODO: add train schedule events


        return Response(events)  