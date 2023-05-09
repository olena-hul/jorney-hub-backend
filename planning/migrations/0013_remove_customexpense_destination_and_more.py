# Generated by Django 4.1.7 on 2023-05-09 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0012_remove_attraction_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customexpense',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='tripattraction',
            name='destination',
        ),
        migrations.AddField(
            model_name='customexpense',
            name='trip',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='custom_expenses', to='planning.trip'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tripattraction',
            name='trip',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='trip_attractions', to='planning.trip'),
            preserve_default=False,
        ),
    ]