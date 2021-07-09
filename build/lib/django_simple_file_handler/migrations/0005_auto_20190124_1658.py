from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_file_handler', '0004_auto_20181005_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporarydocument',
            name='title',
            field=models.CharField(max_length=245),
        ),
        migrations.AlterField(
            model_name='temporarypdf',
            name='title',
            field=models.CharField(max_length=245),
        ),
    ]
