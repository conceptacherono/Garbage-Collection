import email
from django.db import models
from django.forms import DateField
from cloudinary.models import CloudinaryField
# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = CloudinaryField('image',default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location

    def save_events(self):
        self.save()
    
    @classmethod
    def new_events(cls):
        events = cls.objects.all()
        return events
class EventsAttendants(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

    def save_attendees(self):
        self.save()
