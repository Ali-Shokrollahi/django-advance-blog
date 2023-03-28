# Generated by Django 4.1.7 on 2023-03-25 14:02

import apps.profiles.models
import apps.profiles.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, validators=[apps.profiles.validators.CustomUsernameValidator(), django.core.validators.MinLengthValidator(3)])),
                ('first_name', models.CharField(blank=True, max_length=32)),
                ('last_name', models.CharField(blank=True, max_length=32)),
                ('bio', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(default='default_profile_image.png', upload_to=apps.profiles.models.rename_profile_image, verbose_name='profile image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]