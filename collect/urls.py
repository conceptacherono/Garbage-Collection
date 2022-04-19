from unicodedata import name
from django.conf.urls import path
from.import views

urlpatterns=[
    path("",views.home,name='home'),
]