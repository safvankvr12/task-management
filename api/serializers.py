
from rest_framework import serializers
from django.contrib.auth.models import User

from tasks.models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

    def validate(self, data):
        status = data.get('status')
        report = data.get('completion_report')
        hours = data.get('worked_hours')

        if status == 'completed':
            if not report:
                raise serializers.ValidationError({
                    'completion_report': 'This field is required when task is completed.'
                })
            if hours in (None, ''):
                raise serializers.ValidationError({
                    'worked_hours': 'This field is required when task is completed.'
                })
        return data


class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'completion_report', 'worked_hours']