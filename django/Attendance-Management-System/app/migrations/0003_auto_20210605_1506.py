# Generated by Django 3.2.4 on 2021-06-05 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210604_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='stu',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='content',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.examcontent'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='author',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='cid',
            field=models.ForeignKey(default='null', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app.classinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='major',
            field=models.ForeignKey(default='null', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app.majorinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.usertype'),
        ),
    ]