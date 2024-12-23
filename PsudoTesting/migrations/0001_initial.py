# Generated by Django 4.2.16 on 2024-10-10 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Content",
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
                ("text", models.TextField()),
                ("file", models.FileField(upload_to="files/")),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
    ]
