# Generated by Django 4.1.7 on 2023-05-20 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0014_alter_customimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customexpense',
            name='attraction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_expenses', to='planning.attraction'),
        ),
    ]