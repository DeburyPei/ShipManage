# Generated by Django 3.2 on 2023-04-29 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_port_shipinfo_shiptype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipinfo',
            name='build_time',
        ),
    ]
