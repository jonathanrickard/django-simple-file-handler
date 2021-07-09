from django.db import migrations, models
import django_simple_file_handler.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0006_auto_20190429_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatedocument',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='privatedocument',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='privatedocument',
            name='proxy_slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='privatedocument',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='proxy_slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='privatepdf',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='processedimage',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='publicdocument',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='publicpdf',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='temporarydocument',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='generated_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='unprocessedimage',
            name='saved_file',
            field=models.FileField(max_length=255, upload_to=django_simple_file_handler.models.create_file_path, verbose_name='uploaded file'),
        ),
    ]
