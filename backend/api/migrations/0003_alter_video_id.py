# Generated by Django 3.2.7 on 2023-08-29 02:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fd560726-e52b-4f89-838a-aa3d6aab4956'), editable=False, primary_key=True, serialize=False),
        ),
    ]
