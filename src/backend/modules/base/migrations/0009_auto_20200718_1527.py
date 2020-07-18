# Generated by Django 3.0.7 on 2020-07-18 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_oyuuserprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ctfchallenge',
            name='name',
        ),
        migrations.AddField(
            model_name='ctfchallenge',
            name='title',
            field=models.CharField(default='null', max_length=100, unique=True, verbose_name='Гарчиг'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='category',
            field=models.CharField(choices=[('miscellaneous', 'misc'), ('cryptography', 'crypto'), ('forensics', 'forensics'), ('reverse engineering', 're'), ('web exploitation', 'web'), ('binary exploitation', 'pwn')], max_length=100, null=True, verbose_name='Төрөл'),
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Бодлогын өгүүлбэр'),
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='flag',
            field=models.CharField(max_length=100, verbose_name='Flag'),
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='solved_users_count',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='Бодсон хэрэглэгчдийн тоо'),
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='state',
            field=models.CharField(default='active', max_length=100, null=True, verbose_name='Төлөв'),
        ),
        migrations.AlterField(
            model_name='ctfchallenge',
            name='value',
            field=models.PositiveIntegerField(default=0, verbose_name='Бодлогын оноо'),
        ),
        migrations.CreateModel(
            name='UserChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('solved', 'Бодсон'), ('attempted', 'Оролдло хийсэн')], default='attempted', max_length=100, verbose_name='Төлөв')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.CtfChallenge', verbose_name='Challenge')),
                ('oyu_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Хэрэглэгч')),
            ],
        ),
    ]