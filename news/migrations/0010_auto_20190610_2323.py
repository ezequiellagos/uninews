# Generated by Django 2.1.3 on 2019-06-11 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_region_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universidad',
            name='region',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='news.Region', to_field='numero_region'),
        ),
    ]
