from django.db import migrations, models
import django_simple_file_handler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
                ('proxy_slug', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'document (private)',
                'verbose_name_plural': 'documents (private)',
            },
        ),
        migrations.CreateModel(
            name='PrivatePDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
                ('proxy_slug', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'PDF (private)',
                'verbose_name_plural': 'PDFs (private)',
            },
        ),
        migrations.CreateModel(
            name='ProcessedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('output_width', models.PositiveIntegerField(blank=True, null=True)),
                ('output_height', models.PositiveIntegerField(blank=True, null=True)),
                ('processed_file', models.FileField(blank=True, null=True, upload_to='images/processed/')),
            ],
            options={
                'verbose_name': 'image (processed)',
                'verbose_name_plural': 'images (processed)',
            },
        ),
        migrations.CreateModel(
            name='PublicDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'document (public)',
                'verbose_name_plural': 'documents (public)',
            },
        ),
        migrations.CreateModel(
            name='PublicPDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'PDF (public)',
                'verbose_name_plural': 'PDFs (public)',
            },
        ),
        migrations.CreateModel(
            name='TemporaryDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'document (temporary)',
                'verbose_name_plural': 'documents (temporary)',
            },
        ),
        migrations.CreateModel(
            name='TemporaryPDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'PDF (temporary)',
                'verbose_name_plural': 'PDFs (temporary)',
            },
        ),
        migrations.CreateModel(
            name='UnprocessedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('generated_name', models.CharField(blank=True, max_length=254, null=True)),
                ('extra_text', models.TextField(blank=True)),
                ('saved_file', models.FileField(upload_to=django_simple_file_handler.models.create_file_path)),
                ('title', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'image (unprocessed)',
                'verbose_name_plural': 'images (unprocessed)',
            },
        ),
    ]
