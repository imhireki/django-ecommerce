# Generated by Django 3.2.2 on 2021-05-13 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itempedido',
            options={'verbose_name': 'Item do Pedido', 'verbose_name_plural': 'Itens do Pedido'},
        ),
    ]
