from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Course(models.Model):
    """Modelo para los cursos"""
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class CourseGroup(models.Model):
    """Modelo para los grupos de curso"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(_('name'), max_length=100)
    members = models.ManyToManyField(User, related_name='course_groups')
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"