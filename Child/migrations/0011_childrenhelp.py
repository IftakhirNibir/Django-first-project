# Generated by Django 3.2.6 on 2022-04-19 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Child', '0010_delete_childrenhelp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Childrenhelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Child_name', models.CharField(max_length=122)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=122)),
                ('contact_no', models.CharField(max_length=12)),
                ('desc', models.TextField()),
                ('account_no', models.CharField(max_length=20)),
            ],
        ),
    ]
