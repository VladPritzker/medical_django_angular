# medical_app/migrations/0004_merge.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('medical_app', '0001_initial 2'),
        ('medical_app', '0003_alter_customuser_table'),
    ]

    operations = [
        # Include operations from both 0001_initial 2 and 0003_alter_customuser_table
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # other fields from 0001_initial 2
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='field_name',
            field=models.CharField(max_length=255),
            # other field changes from 0003_alter_customuser_table
        ),
        # any other necessary operations
    ]
