# Generated by Django 2.2.6 on 2019-10-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[(None, 'N/A'), ('FANTASY', 'Fantasy'), ('NOVEL', 'Novel'), ('COOKBOOK', 'Cookbook'), ('BIOGRAPHY', 'Biography')], max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('EN', 'English'), ('PL', 'Polish'), ('FR', 'French'), ('DE', 'German')], default='EN', max_length=2),
        ),
    ]
