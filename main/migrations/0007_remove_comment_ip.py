# Generated by Django 3.1 on 2020-09-02 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='ip',
        ),
    ]
