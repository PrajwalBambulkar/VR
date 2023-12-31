# Generated by Django 4.2.4 on 2023-09-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_name', models.CharField(default='poster1', max_length=250)),
                ('poster1', models.ImageField(blank=True, null=True, upload_to='posterimg')),
                ('poster2', models.ImageField(blank=True, null=True, upload_to='posterimg')),
                ('poster3', models.ImageField(blank=True, null=True, upload_to='posterimg')),
            ],
        ),
    ]
