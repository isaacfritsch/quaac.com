# Generated by Django 5.0.1 on 2024-01-24 19:34

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('espaco', '0002_espaco_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='espaco',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='default-title', editable=False, populate_from='title'),
        ),
    ]
