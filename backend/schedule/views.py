from django.shortcuts import render
from .models import Event
from .forms import UploadForm
from .utils import parse_ics

# handles .ics file upload and parsing 
# each .ics file is stored in media\uic_schedules
def upload_form(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()

            # to-do: ics parsing (create and import parse_ics.py from .utils)
            event = parse_ics(upload.file.path)
    else:
        form = UploadForm()

    return render(request, 'schedule/upload_form.html', {'form': form})

#Send data to frontend
@api_view(['GET'])
def getData(request):
    return Response({"message": "Hello from Django!"})