# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-21 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django_simple_file_handler.functions


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatedocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.functions.create_file_path),
        ),
    ]
