from django.db import models

# holds each class or commute time block
class Event(models.Model):
    title = models.CharField(max_length=200)
    # location = models.CharField(max_length=200, blank=True)
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()
    # building = models.CharField(max_length=50, blank=True)
    # room = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

# holds uploaded .ics files of uic schedule
class UICSchedule(models.Model):
    file = models.FileField(upload_to='uic_schedules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    