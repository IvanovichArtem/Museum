# Generated by Django 4.2.17 on 2024-12-18 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtPiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='art_pieces/')),
                ('artist', models.CharField(max_length=255)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('exhibition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_pieces', to='catalog.exhibition')),
            ],
        ),
    ]