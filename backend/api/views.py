from django.contrib.auth.models import User
from rest_framework import generics
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