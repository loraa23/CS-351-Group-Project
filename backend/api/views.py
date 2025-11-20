from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, ScheduleSerializer
from .metra import get_stations_for_route
from .models import Schedule, Student
from .serializers import UserSerializer

# from .forms import UploadForm
from .utils import parse_ics, generate_commute_schedule, extract_courses_from_events, extract_availability_from_events, ranked_matches_within_group

class ScheduleListCreate(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Schedule.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            file = self.request.FILES.get("file")
            user = self.request.user
            # count = Schedule.objects.filter(author=user).count()
            # title = f"schedule_{count + 1}"
            title = file.name

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
        train_line = request.data.get("train_line")
        station = request.data.get("station")
        user = request.user

        # Get the latest uploaded schedule
        schedule = Schedule.objects.filter(author=user).order_by('-uploaded_at').first()
        if not schedule:
            return Response({"error": "No schedule uploaded"}, status=400)

        # Parse ICS → Python objects
        try:
            # extract class events and add train commute
            events = generate_commute_schedule(schedule.file.path, train_line, station)
           
            # add courses and availability
            student, created = Student.objects.get_or_create(user=request.user)
            extract_courses_from_events(student, events)
            extract_availability_from_events(student, events)

            # study groups testing
            ranked_matches_within_group(student)

        except Exception as e:
            return Response(
                {"error": f"Failed to parse schedule: {e}"},
                status=500
            )
        
        return Response(events)  
    
class GetStations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, route_id):
        stations = get_stations_for_route(route_id)
        return Response(stations)
    
class GetStudentMatches(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student, created = Student.objects.get_or_create(user=request.user)
        matches = ranked_matches_within_group(student)
        return Response(matches)