from django.db import models
from django.contrib.auth.models import User

# holds uploaded .ics files of uic schedule
class Schedule(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uic_schedules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    
    def delete(self, *args, **kwargs):
        self.file.delete(save=False) # delete file from storage
        super().delete(*args, **kwargs) # delete model instance