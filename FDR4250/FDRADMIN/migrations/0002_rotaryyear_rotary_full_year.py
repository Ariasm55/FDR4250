# Generated by Django 5.0.6 on 2024-07-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FDRADMIN', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rotaryyear',
            name='rotary_full_year',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]