# Generated by Django 3.1.2 on 2021-08-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0011_auto_20210821_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='last_used',
            field=models.BooleanField(default=False),
        ),
    ]