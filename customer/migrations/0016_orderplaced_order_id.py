# Generated by Django 4.2.4 on 2023-09-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='order_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
