from multiprocessing import Event
from django.contrib import admin

from collect.models import Events, EventsAttendants, Post, Rating, ReviewRating

# Register your models here.
admin.site.register(Events)
admin.site.register(EventsAttendants)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(ReviewRating)