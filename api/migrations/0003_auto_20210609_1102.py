# Generated by Django 3.2.2 on 2021-06-09 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210605_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
