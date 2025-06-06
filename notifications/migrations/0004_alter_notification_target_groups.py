# Generated by Django 5.2.1 on 2025-05-30 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_created_at_remove_course_updated_at'),
        ('notifications', '0003_notification_target_campuses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='target_groups',
            field=models.ManyToManyField(blank=True, related_name='notifications', to='courses.coursegroup'),
        ),
    ]
