from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer, NotificationDetailSerializer
from courses.models import CourseGroup
from users.models import User
from utils.push_service import send_push_notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'message', 'type']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        user_groups = CourseGroup.objects.filter(members=request.user)
        notifications = Notification.objects.filter(
            target_groups__in=user_groups
        ).distinct().order_by('-created_at')
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def send(self, request, pk=None):
        notification = self.get_object()

        if notification.sent:
            return Response({'detail': 'Notification already sent'}, status=400)

        # Get users from target groups
        users_from_groups = User.objects.filter(
            coursegroup__in=notification.target_groups.all()
        )


        # Get users from target campuses (sedes)
        users_from_campuses = User.objects.filter(
            student__campus__in=notification.target_campuses
        )


        # Get users by specific email addresses
        users_from_emails = User.objects.filter(
            email__in=notification.target_emails
        )

        # Merge all users without duplication
        recipients = set(users_from_groups) | set(users_from_campuses) | set(users_from_emails)

        # Send notification to each user with push token
        for user in recipients:
            if user.push_token:
                send_push_notification(
                    user.push_token,
                    notification.title,
                    notification.message,
                    {'type': notification.type}
                )

        # Mark notification as sent
        notification.sent = True
        notification.save()

        return Response({'status': 'notification sent'})
