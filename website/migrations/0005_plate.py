# Generated by Django 4.0.3 on 2022-05-29 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_vase_vaseref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('plateId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('imageRef', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
