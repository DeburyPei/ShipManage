# Generated by Django 3.2 on 2023-04-29 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_cargo_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.cargo')),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.shipinfo')),
            ],
        ),
    ]
