# Generated by Django 2.1.2 on 2018-10-19 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='folowed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
