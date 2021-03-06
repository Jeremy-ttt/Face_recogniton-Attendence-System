# Generated by Django 3.0.3 on 2021-06-04 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='stu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.UserInfo'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.ExamContent'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.UserInfo'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.UserInfo'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.UserInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='cid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.ClassInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='major',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.MajorInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.UserType'),
        ),
    ]
