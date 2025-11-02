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
            serializer.save(author=self.request.user)
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


# handles .ics file upload and parsing 
# each .ics file is stored in media\uic_schedules
# def upload_form(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             upload = form.save()

#             # to-do: ics parsing (create and import parse_ics.py from .utils)
#             event = parse_ics(upload.file.path)
#     else:
#         form = UploadForm()

#     return render(request, 'schedule/upload_form.html', {'form': form})

