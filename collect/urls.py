
from unicodedata import name
from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('events/',views.current_events,name='events'),
    path('attend/',views.attend_event,name='attend')
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)