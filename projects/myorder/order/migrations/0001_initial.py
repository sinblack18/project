# Generated by Django 4.1.7 on 2023-03-23 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("order_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("order_text", models.TextField()),
                ("price", models.IntegerField(default=0)),
                ("address", models.CharField(max_length=200)),
            ],
        ),
    ]