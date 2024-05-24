# medical_app/migrations/0002_rename_customuser_table.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('medical_app', '0001_initial'),  # Adjust this to the correct dependency
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]
