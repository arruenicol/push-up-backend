from django.db import models
from django.utils.translation import gettext_lazy as _
from courses.models import CourseGroup
from users.models import User

class NotificationType(models.TextChoices):
    SCHEDULE_CHANGE = 'schedule', _('Cambio de Horario')
    ROOM_CHANGE = 'room', _('Cambio de Sala')
    SUSPENSION = 'suspension', _('Suspensión de Clases')
    ANNOUNCEMENT = 'announcement', _('Aviso')


class Notification(models.Model):
    """Modelo para las notificaciones"""
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))
    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.ANNOUNCEMENT
    )
    target_groups = models.ManyToManyField(CourseGroup, blank=True, related_name='notifications')
    target_emails = models.JSONField(default=list, blank=True)  # lista de correos individuales
    target_campuses = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

class NotificacionUsuario(models.Model):
    """Registro de envío y lectura de notificaciones por usuario"""
    notificacion = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='recepciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    enviada = models.BooleanField(default=False)
    leida = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'notificación usuario'
        verbose_name_plural = 'notificaciones usuario'
        unique_together = ('notificacion', 'usuario')
    
    def __str__(self):
        return f"{self.notificacion.title} - {self.usuario.email}"