# Generated by Django 4.2.6 on 2023-10-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airplane",
            name="name",
            field=models.CharField(max_length=63, unique=True),
        ),
        migrations.AlterField(
            model_name="airport",
            name="name",
            field=models.CharField(max_length=127, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="crew",
            unique_together={("first_name", "last_name")},
        ),
        migrations.AlterUniqueTogether(
            name="route",
            unique_together={("source", "destination")},
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("row", "seat", "flight")},
        ),
    ]
