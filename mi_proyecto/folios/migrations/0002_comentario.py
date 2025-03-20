# Generated by Django 5.1.7 on 2025-03-08 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Comentario')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('hora', models.TimeField(auto_now_add=True, verbose_name='Hora')),
                ('folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_folio', to='folios.folio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
