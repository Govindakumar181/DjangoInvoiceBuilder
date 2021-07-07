# Generated by Django 3.0.4 on 2021-07-05 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentportalapp', '0002_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer_project',
            new_name='customer_project_title',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='posting_date',
        ),
        migrations.AddField(
            model_name='customer',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 5, 20, 5, 1, 949491)),
        ),
        migrations.AddField(
            model_name='customer',
            name='milestone',
            field=models.IntegerField(default='00'),
        ),
        migrations.AddField(
            model_name='customer',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 5, 20, 5, 1, 949491)),
        ),
        migrations.AddField(
            model_name='customer',
            name='total_cost',
            field=models.IntegerField(default='00'),
        ),
    ]