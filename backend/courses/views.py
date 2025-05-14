from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, CourseGroup
from .serializers import CourseSerializer, CourseGroupSerializer, CourseGroupDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseGroupDetailSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        groups = CourseGroup.objects.filter(members=request.user)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)