from.email import send_join_email
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from collect.forms import EventAttendForm

from collect.models import Events, EventsAttendants
# Create your views here.
def home(request):
    return render(request,'home.html')

def current_events(request):
    events = Events.objects.all()
    return render(request,'all-garbage/events.html',{"events":events})

def attend_event(request):
    if request.method == 'POST':
        form = EventAttendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            recepient = EventsAttendants(name=name,email=email)
            recepient.save()
            send_join_email(name,email)
            HttpResponseRedirect('attend')
    else:
        form = EventAttendForm()
    return render(request,'all-garbage/attend.html',{"attendForm":form})