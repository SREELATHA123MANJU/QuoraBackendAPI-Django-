# Generated by Django 3.1.1 on 2020-09-04 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='testapp.question')),
            ],
        ),
    ]
