# Generated by Django 5.1.1 on 2024-12-23 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_contactdetails_blog_main_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='image_url',
        ),
    ]
