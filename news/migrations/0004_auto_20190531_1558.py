# Generated by Django 2.1.3 on 2019-05-31 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20181210_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universidad',
            name='region',
            field=models.CharField(choices=[('1', 'Tarapacá'), ('2', 'Antofagasta'), ('3', 'Atacama'), ('4', 'Coquimbo'), ('5', 'Valparaíso'), ('6', "Libertador Bernardo O'Higgins"), ('7', 'Maule'), ('8', 'Concepción'), ('9', 'Araucanía'), ('10', 'Los Lagos'), ('11', 'Aysén del Gral Carlos Ibáñez del Campo'), ('12', 'Magallanes y de la Antártica Chilena'), ('13', 'Metropolitana'), ('14', 'Los Ríos'), ('15', 'Arica y Parinacota'), ('16', 'Ñuble ')], max_length=2),
        ),
    ]
