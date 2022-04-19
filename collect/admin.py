from multiprocessing import Event
from django.contrib import admin

from collect.models import Events

# Register your models here.
admin.site.register(Events)