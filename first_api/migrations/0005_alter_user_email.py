# Generated by Django 4.2.2 on 2024-02-07 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_api', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
