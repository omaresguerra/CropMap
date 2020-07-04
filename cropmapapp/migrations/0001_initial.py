# Generated by Django 2.0 on 2020-07-04 05:09

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
            name='Comparison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw', models.CharField(max_length=1000)),
                ('croppingdate', models.DateField()),
                ('description', models.CharField(max_length=2000)),
                ('graph', models.CharField(max_length=1000)),
                ('ndvipiegraph', models.CharField(max_length=1000)),
                ('osavipiegraph', models.CharField(max_length=1000)),
                ('croppingdata', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='CroppingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cropping', models.FileField(upload_to='')),
                ('croppingdate', models.DateField()),
                ('description', models.CharField(max_length=2000)),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CroppingDataDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw', models.CharField(max_length=1000)),
                ('ndvi', models.CharField(max_length=1000)),
                ('osavi', models.CharField(max_length=1000)),
                ('ndvi_4x4', models.CharField(max_length=1000)),
                ('osavi_4x4', models.CharField(max_length=1000)),
                ('graph', models.CharField(max_length=1000)),
                ('ndvipiegraph', models.CharField(max_length=1000)),
                ('osavipiegraph', models.CharField(max_length=1000)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropmapapp.CroppingData')),
            ],
        ),
        migrations.CreateModel(
            name='CroppingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surveying_area', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=1000)),
                ('land_description', models.CharField(max_length=2000)),
                ('image_raw', models.FileField(upload_to='')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw', models.CharField(max_length=1000)),
                ('ndvi', models.CharField(max_length=1000)),
                ('osavi', models.CharField(max_length=1000)),
                ('ndvi_4x4', models.CharField(max_length=1000)),
                ('osavi_4x4', models.CharField(max_length=1000)),
                ('graph', models.CharField(max_length=1000)),
                ('ndvipiegraph', models.CharField(max_length=1000)),
                ('osavipiegraph', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=1000)),
                ('image_description', models.CharField(max_length=2000)),
                ('image_raw', models.FileField(upload_to='')),
                ('processed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='data',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropmapapp.Image'),
        ),
        migrations.AddField(
            model_name='croppingdata',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropmapapp.CroppingImage'),
        ),
        migrations.AddField(
            model_name='comparison',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cropmapapp.CroppingImage'),
        ),
    ]
