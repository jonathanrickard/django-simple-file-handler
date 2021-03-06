from django.db import migrations, models
import django_simple_file_handler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0005_auto_20190124_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatedocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='processed_file',
            field=models.FileField(blank=True, null=True, upload_to=django_simple_file_handler.models.create_image_path),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='privatedocument',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='extra_text',
            field=models.TextField(blank=True, verbose_name='extra text (optional)'),
        ),
    ]
