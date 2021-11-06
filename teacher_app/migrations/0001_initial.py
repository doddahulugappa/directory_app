# Generated by Django 3.2.4 on 2021-10-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=12, null=True)),
                ('room_number', models.CharField(max_length=12, null=True)),
                ('subjects_taught', models.ManyToManyField(blank=True, to='teacher_app.Subject')),
            ],
        ),
    ]
