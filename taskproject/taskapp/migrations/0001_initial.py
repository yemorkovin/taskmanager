# Generated by Django 5.0 on 2023-12-13 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=255)),
                ('Description', models.TextField(blank=True)),
                ('Status', models.CharField(max_length=50)),
                ('Priority', models.IntegerField()),
                ('Start', models.DateTimeField()),
                ('End', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TeamName', models.CharField(max_length=100)),
                ('CreationDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastName', models.CharField(max_length=50)),
                ('FirstName', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('HashedPassword', models.CharField(max_length=200)),
                ('CreationDate', models.DateTimeField(auto_now=True)),
                ('Role', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TaskContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comments', models.TextField(blank=True)),
                ('ChangeHistory', models.TextField(blank=True)),
                ('Attachments', models.TextField(blank=True)),
                ('TaskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.task')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JoinDate', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.user')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='AssignedUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.user'),
        ),
    ]
