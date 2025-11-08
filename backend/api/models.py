from django.db import models
from django.contrib.auth.models import User

# holds uploaded .ics files of uic schedule
class Schedule(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uic_schedules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    