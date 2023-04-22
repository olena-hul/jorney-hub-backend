# Generated by Django 4.1.7 on 2023-04-22 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("planning", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TripAttraction",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateTimeField()),
                ("visited", models.BooleanField(default=False)),
                ("note", models.TextField(null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("currency", models.CharField(max_length=3, null=True)),
                (
                    "attraction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_attractions",
                        to="planning.location",
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_attractions",
                        to="planning.destination",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trips",
                        to="planning.destination",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trips",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Attraction",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                (
                    "attraction_type",
                    models.CharField(
                        choices=[
                            ("Museum", "Museum"),
                            ("Art Gallery", "Art Gallery"),
                            ("Historic Site", "Historic Site"),
                            ("Park", "Park"),
                            ("Zoo", "Zoo"),
                            ("Aquarium", "Aquarium"),
                            ("Amusement Park", "Amusement Park"),
                            ("Theater", "Theater"),
                            ("Concert Hall", "Concert Hall"),
                            ("Stadium", "Stadium"),
                            ("Sports Complex", "Sports Complex"),
                            ("Shopping Mall", "Shopping Mall"),
                            ("Market", "Market"),
                            ("Restaurant", "Restaurant"),
                            ("Bar", "Bar"),
                            ("Nightclub", "Nightclub"),
                        ],
                        max_length=255,
                    ),
                ),
                ("rating", models.FloatField(default=0)),
                ("ratings_count", models.IntegerField(default=0)),
                ("views_count", models.IntegerField(default=0)),
                ("address", models.CharField(max_length=255)),
                ("image_urls", models.JSONField(null=True)),
                ("duration", models.IntegerField(default=1)),
                (
                    "budget_category",
                    models.CharField(
                        choices=[
                            ("Accommodation", "Accommodation"),
                            ("Transportation", "Transportation"),
                            ("Food and Drink", "Food and Drink"),
                            (
                                "Activities and Entertainment",
                                "Activities and Entertainment",
                            ),
                            ("Shopping", "Shopping"),
                            ("Miscellaneous", "Miscellaneous"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attractions",
                        to="planning.destination",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attractions",
                        to="planning.location",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]