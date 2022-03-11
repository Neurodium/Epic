# Generated by Django 4.0.2 on 2022-03-09 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epicevent', '0002_event_attendees_event_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contract_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_contract', to='epicevent.contract'),
            preserve_default=False,
        ),
    ]