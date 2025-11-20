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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    course_code = models.CharField(max_length=20)   # e.g., "CS341"
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_code
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} in {self.course}"
    
class Availability(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    day_of_week = models.IntegerField()  
    # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.student} {self.day_of_week}: {self.start_time}-{self.end_time}"