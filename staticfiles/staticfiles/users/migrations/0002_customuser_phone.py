# Generated by Django 4.0.4 on 2022-04-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
