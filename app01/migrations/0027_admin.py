# Generated by Django 3.2 on 2023-05-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0026_alter_order_remark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
    ]