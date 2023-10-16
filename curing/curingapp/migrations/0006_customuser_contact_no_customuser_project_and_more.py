# Generated by Django 4.1.7 on 2023-09-25 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curingapp', '0005_transaction_concreting_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='contact_no',
            field=models.CharField(default='NA', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='curingapp.project_master'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='curingapp.site_master'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
