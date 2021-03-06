# Generated by Django 3.2.4 on 2021-06-05 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210605_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='stu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.examcontent'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.userinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='cid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.classinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.majorinfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.usertype'),
        ),
    ]
