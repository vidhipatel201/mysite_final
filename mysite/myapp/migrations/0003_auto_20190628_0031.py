# Generated by Django 2.1.3 on 2019-06-28 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190627_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='pic',
            field=models.ImageField(blank=True, upload_to='userImages/'),
        ),
    ]
