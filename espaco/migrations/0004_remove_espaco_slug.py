# Generated by Django 5.0.1 on 2024-01-24 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('espaco', '0003_alter_espaco_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='espaco',
            name='slug',
        ),
    ]
