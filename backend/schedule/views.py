from django.shortcuts import render
from .models import Event
from .forms import UploadForm


# from tutorial, not needed in final project
def events_list(request):
    events = Event.objects.all()
    return render(request, 'schedule/events_list.html', {'events':events})

# handles .ics file upload and parsing 
# each .ics file is stored in media\uic_schedules
def upload_form(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()

            # to-do: ics parsing (create and import parse_ics from .utils)
    else:
        form = UploadForm()

    return render(request, 'schedule/upload_form.html', {'form': form})