# Generated by Django 5.0.1 on 2024-05-27 03:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('espaco', '0002_initial'),
        ('questoes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questao',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='espaco.espaco'),
        ),
        migrations.AddField(
            model_name='questao',
            name='tags',
            field=models.ManyToManyField(to='espaco.tag'),
        ),
        migrations.AddField(
            model_name='questao',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='questao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questoes.questao'),
        ),
        migrations.AddField(
            model_name='reply',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='questoes.comment'),
        ),
        migrations.AddField(
            model_name='replysolucao',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resolucao',
            name='questao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questoes.questao'),
        ),
        migrations.AddField(
            model_name='resolucao',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solucao',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solucao',
            name='questao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questoes.questao'),
        ),
        migrations.AddField(
            model_name='replysolucao',
            name='solucao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies_solucao', to='questoes.solucao'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='resolucao',
            unique_together={('user', 'questao')},
        ),
    ]
