# Generated by Django 2.2.5 on 2020-05-18 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Comment goes here...')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='None', unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Reply goes here...')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Your title...')),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='post_images', verbose_name='Image')),
                ('content', models.TextField()),
                ('choice1', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('1', 'Art'), ('2', 'Buisness'), ('3', 'Cooking'), ('4', 'Design'), ('5', 'Education'), ('6', 'Engineering'), ('7', 'Entertainment'), ('8', 'Food'), ('9', 'Goverment')], max_length=17, verbose_name='Category')),
                ('choice2', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('10', 'Healthcare'), ('11', 'Languages'), ('12', 'Law'), ('13', 'Mathematics'), ('14', 'Politics'), ('15', 'Science'), ('16', 'Sports'), ('17', 'Technology'), ('18', 'Traveling')], max_length=26, verbose_name='Category')),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]
