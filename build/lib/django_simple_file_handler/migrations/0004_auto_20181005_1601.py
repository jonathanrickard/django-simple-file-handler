from django.db import migrations, models
import django_simple_file_handler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0003_auto_20180525_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatepdf',
            name='template_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publicpdf',
            name='template_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='temporarypdf',
            name='template_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='privatedocument',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='processed_file',
            field=models.FileField(blank=True, null=True, upload_to=django_simple_file_handler.models.create_image_path),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='title',
            field=models.CharField(max_length=245, unique=True),
        ),
    ]
