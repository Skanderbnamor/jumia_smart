# Generated by Django 5.0.4 on 2024-05-21 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumia', '0002_alter_smartphone_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartphone',
            name='image',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
