# Generated by Django 5.0.6 on 2024-06-27 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_app', '0008_remove_healthhistory_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AlterModelTable(
            name='customuser',
            table=None,
        ),
    ]
