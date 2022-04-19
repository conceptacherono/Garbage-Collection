from asyncio import events
from django.test import TestCase

from collect.models import Events

# Create your tests here.
class EventsTestClass(TestCase):
    def setUp(self):
        self.event = Events(name="street cleaning",description='we shall meet to clean nairobi river',location='nairobi',image='/image',date='11-02-2022')
        self.event.save_events()

    def test_instance(self):
        self.assertTrue(isinstance(self.event,Events))

    def test_save_event(self):
        self.event.save_events()
        events = Events.objects.all()
        self.assertTrue(len(events) > 0)

    def test_get_events(self):
        events_comming = Events.new_events()
        self.assertTrue(len(events_comming)>0)
