# Generated by Django 5.2 on 2025-05-05 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_experience_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
