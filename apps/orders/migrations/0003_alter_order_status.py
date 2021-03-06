# Generated by Django 3.2.6 on 2021-11-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('progress', 'In Progress'), ('accepted', 'Accepted'), ('shipped', 'Shipped'), ('completed', 'Completed')], default='In Progress', max_length=20),
        ),
    ]
