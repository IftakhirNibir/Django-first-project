# Generated by Django 3.2.6 on 2022-05-04 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Child', '0028_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='customer',
        ),
    ]
