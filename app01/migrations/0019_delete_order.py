# Generated by Django 3.2 on 2023-05-02 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0018_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]