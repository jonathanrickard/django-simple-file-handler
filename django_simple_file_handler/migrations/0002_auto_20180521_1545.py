from django.db import migrations, models
import django_simple_file_handler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatedocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='saved_file',
            field=models.FileField(max_length=254, upload_to=django_simple_file_handler.models.create_file_path),
        ),
    ]
