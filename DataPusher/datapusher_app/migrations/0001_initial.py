# Generated by Django 4.1.3 on 2023-06-15 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("account_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=100)),
                ("account_name", models.CharField(max_length=100)),
                (
                    "app_secret_token",
                    models.CharField(blank=True, max_length=100, unique=True),
                ),
                ("website", models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Destination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("http_method", models.CharField(max_length=100)),
                ("headers", models.JSONField()),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datapusher_app.account",
                    ),
                ),
            ],
        ),
    ]
