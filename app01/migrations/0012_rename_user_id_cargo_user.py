# Generated by Django 3.2 on 2023-04-29 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_cargo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo',
            old_name='user_id',
            new_name='user',
        ),
    ]
