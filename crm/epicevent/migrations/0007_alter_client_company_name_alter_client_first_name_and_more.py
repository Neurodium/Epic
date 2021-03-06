# Generated by Django 4.0.2 on 2022-03-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epicevent', '0006_remove_contract_signed_alter_contract_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
