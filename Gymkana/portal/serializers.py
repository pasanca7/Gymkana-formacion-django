from portal.models import Event
from rest_framework import serializers

class event_serializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
            start_date = data['start_date']
            end_date = data['end_date']
            """
            start_date must be before end_start
            """
            if start_date > end_date:
                raise serializers.ValidationError('La fecha de comienzo no puede ser posterior a la fin', code = 'invalid_dates')

            return data