# Generated by Django 4.2.17 on 2024-12-18 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_remove_artpiece_artist_remove_artpiece_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artpiece',
            name='title',
        ),
    ]