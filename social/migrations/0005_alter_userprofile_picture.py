# Generated by Django 3.2.9 on 2021-12-01 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_userprofile_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='uploads/profile_pictures/terrier2.jpg', upload_to='uploads/profile_pictures'),
        ),
    ]
