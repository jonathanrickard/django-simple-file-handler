from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0007_auto_20210514_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatepdf',
            options={'verbose_name': 'Generated PDF (private)', 'verbose_name_plural': 'Generated PDFs (private)'},
        ),
        migrations.AlterModelOptions(
            name='publicpdf',
            options={'verbose_name': 'Generated PDF (public)', 'verbose_name_plural': 'Generated PDFs (public)'},
        ),
        migrations.AlterModelOptions(
            name='temporarypdf',
            options={'verbose_name': 'Generated PDF (temporary)', 'verbose_name_plural': 'Generated PDFs (temporary)'},
        ),
    ]
