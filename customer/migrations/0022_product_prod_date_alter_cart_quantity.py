# Generated by Django 4.2.4 on 2023-10-04 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_userprofile_sellerproduct_sellerapprovedproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
