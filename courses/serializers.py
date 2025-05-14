from rest_framework import serializers
from .models import Course, CourseGroup
from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'created_at')
        read_only_fields = ('id', 'created_at')


class CourseGroupSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseGroup
        fields = ('id', 'name', 'course', 'members_count')
        read_only_fields = ('id',)
    
    def get_members_count(self, obj):
        return obj.members.count()


class CourseGroupDetailSerializer(CourseGroupSerializer):
    members = UserSerializer(many=True, read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta(CourseGroupSerializer.Meta):
        fields = CourseGroupSerializer.Meta.fields + ('members',)
