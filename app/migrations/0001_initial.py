# Generated by Django 5.1.1 on 2024-12-10 20:58

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(default='UNKNOWN', max_length=200)),
                ('content', models.TextField()),
                ('read_time', models.IntegerField(blank=True, null=True)),
                ('trend', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', models.URLField()),
                ('author_image', models.URLField(default='https://png.pngtree.com/png-vector/20221110/ourmid/pngtree-silhouette-of-anonymous-man-in-mugshot-lineup-isolated-on-white-background-png-image_6441511.png')),
                ('category', models.ManyToManyField(blank=True, null=True, related_name='blogs', to='app.category')),
                ('tag', models.ManyToManyField(blank=True, null=True, to='app.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True, null=True)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.blog')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.comment')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('paragraph', 'Paragraph'), ('quote', 'Quote'), ('link', 'Link'), ('image', 'Image'), ('heading', 'heading')], max_length=20)),
                ('text_content', models.TextField(blank=True, null=True)),
                ('author', models.CharField(default='UNKNOWN', max_length=200)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('link_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='app.blog')),
            ],
        ),
        migrations.CreateModel(
            name='RandomRedirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genrated_redirections_id', models.CharField(max_length=25, unique=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.blog')),
            ],
        ),
        migrations.CreateModel(
            name='RedirectBlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redirectblogs', to='app.blog')),
                ('configuration', models.ManyToManyField(related_name='redirectblogs_configuration', to='app.blog')),
            ],
        ),
        migrations.CreateModel(
            name='MainRedirections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirections_id', models.CharField(max_length=255, unique=True)),
                ('final_link', models.URLField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_redirections', to='app.task')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=app.models.generate_user_id, max_length=50, unique=True)),
                ('redirection_history', models.ManyToManyField(related_name='redirected_users', to='app.blog')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.task')),
            ],
        ),
    ]
