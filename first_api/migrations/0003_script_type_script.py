# Generated by Django 4.2.2 on 2023-11-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0002_alter_script_repository_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='type_script',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
