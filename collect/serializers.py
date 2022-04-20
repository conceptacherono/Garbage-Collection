from rest_framework import serializers
from collect.models import Events

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id','name','description','location','image','date')