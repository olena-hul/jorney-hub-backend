# Generated by Django 4.1.7 on 2023-05-09 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planning', '0010_customexpense'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='rates',
            field=models.ManyToManyField(related_name='attractions', to='ratings.rate'),
        ),
        migrations.AddField(
            model_name='destination',
            name='rates',
            field=models.ManyToManyField(related_name='destinations', to='ratings.rate'),
        ),
        migrations.CreateModel(
            name='CustomImage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.TextField()),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_images', to='planning.attraction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
