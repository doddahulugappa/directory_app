# Generated by Django 3.2.4 on 2021-10-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory_app', '0003_delete_usermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]
