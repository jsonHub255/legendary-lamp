# Generated by Django 4.2 on 2023-04-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='SKU',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
    ]
