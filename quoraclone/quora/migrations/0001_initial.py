# Generated by Django 4.1.5 on 2023-01-24 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import quora.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('votes', models.IntegerField(default=0)),
                ('accepted', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=quora.models.Profile.upload_location)),
                ('location', models.TextField(default='Not mentioned')),
                ('points', models.IntegerField(default=0)),
                ('questions', models.IntegerField(default=0)),
                ('answers', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quora.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('answers', models.IntegerField(default=0)),
                ('answered', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quora.profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quora.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quora.profile'),
        ),
    ]
