# Generated by Django 4.2.4 on 2023-09-04 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_product_back_image_alter_product_left_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='back_image',
            field=models.ImageField(blank=True, null=True, upload_to='productimg'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('TS', 'Clothes'), ('AC', 'Accessories'), ('BK', 'Books'), ('PT', 'Painting')], max_length=15),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='productimg'),
        ),
    ]
