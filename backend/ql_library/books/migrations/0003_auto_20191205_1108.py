# Generated by Django 2.2.8 on 2019-12-05 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20191030_1008'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('author', 'title', 'language')},
        ),
    ]
