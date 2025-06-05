from rest_framework import serializers
from .models import Notification
from courses.serializers import CourseGroupSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'title', 'message', 'type', 'target_groups',
            'target_emails', 'target_campuses',
            'created_at', 'scheduled_for', 'sent'
        )
        read_only_fields = ('id', 'created_at', 'sent')


class NotificationDetailSerializer(NotificationSerializer):
    target_groups = CourseGroupSerializer(many=True, read_only=True)