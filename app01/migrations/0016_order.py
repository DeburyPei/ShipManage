# Generated by Django 3.2 on 2023-04-29 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_delete_order'),
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
                ('end_port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_port', to='app01.port')),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.shipinfo')),
                ('start_port', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_port', to='app01.port')),
            ],
        ),
    ]
