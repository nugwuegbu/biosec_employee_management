from django.db import models

# Create your models here.

class Employee(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    first_name  = models.CharField(max_length=100,blank=False)
    last_name  = models.CharField(max_length=100,blank=False)
    email  = models.CharField(max_length=100,blank=False)
    phone  = models.CharField(max_length=20,blank=False)
    job_title = models.CharField(max_length=100,blank=False)
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name

class ActivityLogs(models.Model):
    activity_name =models.CharField(max_length=20)
    activity_time = models.DateTimeField();
    activity_request = models.TextField()
    activity_response = models.TextField()
    user = models.IntegerField()

    def __str__(self):
        return self.activity_name

