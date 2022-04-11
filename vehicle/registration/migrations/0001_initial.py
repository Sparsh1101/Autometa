# Generated by Django 4.0.3 on 2022-04-09 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fName', models.BinaryField()),
                ('lName', models.BinaryField()),
                ('aadhar', models.BinaryField(null=True)),
                ('email', models.BinaryField(null=True)),
                ('mobileNo', models.BinaryField(null=True)),
                ('gender', models.BinaryField()),
                ('dob', models.BinaryField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
