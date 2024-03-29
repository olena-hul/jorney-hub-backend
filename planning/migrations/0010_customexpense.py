# Generated by Django 4.1.7 on 2023-05-09 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0009_alter_tripattraction_attraction'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomExpense',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.CharField(max_length=3, null=True)),
                ('budget_category', models.CharField(choices=[('Accommodation', 'Accommodation'), ('Transportation', 'Transportation'), ('Food and Drink', 'Food and Drink'), ('Activities', 'Activities'), ('Shopping', 'Shopping'), ('Miscellaneous', 'Miscellaneous')], max_length=255)),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_expenses', to='planning.attraction')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_expenses', to='planning.destination')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
