# Generated by Django 2.2.4 on 2019-10-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LineNotifyToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=100, verbose_name='別名')),
                ('token', models.CharField(max_length=50, verbose_name='token')),
            ],
        ),
        migrations.CreateModel(
            name='LineNotifyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名稱')),
                ('members', models.ManyToManyField(to='line.LineNotifyToken', verbose_name='成員')),
            ],
        ),
    ]