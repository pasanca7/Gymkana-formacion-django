from portal.models import Event
from rest_framework import serializers

class event_serializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
