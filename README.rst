==========================
django-simple-file-handler
==========================

The django-simple-file-handler package is an app for uploading and managing documents and images. With optional packages installed, it can process images and generate PDFs from HTML files. It has only been tested with Django 1.11 and Python 3.6.

If python-magic is installed, django-simple-file-handler will use it to check uploaded file MIME types. Otherwise, it will use Python's built-in library. This package has only been tested with python-magic 0.4.

Please note that "private" files and PDFs would more accurately be described as "hidden." The app generates a proxy URL that will load the file for a logged-in user and stores the file with a name consisting of many random characters. Still, it is possible to load these files without logging in if the file name is known.

Processed image generation requires that Pillow be installed. This package has only been tested with Pillow 5.0.

PDF generation requires that either WeasyPrint or xhtml2pdf be installed. This package has only been tested with WeasyPrint 0.28 and xhtml2pdf 0.2.1. Please refer to those projects' documentation for HTML template-formatting specifics.

-----------
Quick start
-----------

1. Run ``pip install django-simple-file-handler``.

2. Add django-simple-file-handler to your installed apps: ::

    INSTALLED_APPS = (
        ...
        'django_simple_file_handler',
        
    )

3. Run ``python manage.py migrate``.

4. Include the django-simple-file-handler URLconf in your project urls.py like this (this step is only required if you wish to use private files or PDFs): ::

    urlpatterns = [
        ...
        url(r'^private_file_pseudo_directory_path/', include('django_simple_file_handler.urls')),
    ]

------
Basics
------

Files are deleted or replaced when their corresponding model instances are deleted or changed.

Public and private documents, as well as unprocessed images, can be created and managed via the admin site. Other types are read-only in the admin site.

The proxy URL for a private document or pdf can be accessed at ``model_instance.proxy_url``.

Temporary documents and PDFs are intended to be used for objects that might need to have the same title.

All types can be created and accessed by subclassing or creating a foreign key in your own apps, but temporary documents, processed images and public or private PDFs must be created this way. Here are some basic examples:

**Temporary document** ::

    from django_simple_file_handler.models import TemporaryDocument

    class MyModel(models.Model):
        ...
        document_instance = TemporaryDocument(
            title = 'Your Temporary Document Title',
            extra_text = 'Any associated text you might need (optional)',
            saved_file = file_from_your_app,
        )
        document_instance.save()

**Processed image** ::

    from django_simple_file_handler.models import ProcessedImage

    class MyModel(models.Model):
        ...
        image_instance = ProcessedImage(
            extra_text = 'Any associated text you might need (optional)',
            output_width = 200,
            output_height = 100,
            saved_file = file_from_your_app,
        )
        image_instance.save()
    
The resized and/or cropped image can then be accessed at ``image_instance.processed_file``.

**Public generated PDF** ::

    from django_simple_file_handler.models import PublicPDF

    class MyModel(models.Model):
        ...
        kwargs = {
            'template_location' : 'path/to/your/html_template.html',
            'data' : {
                'value_one': 'First value in your HTML template',
                'value_two': 'Second value in your HTML template',
                'value_three': 'Third value in your HTML template',
            },
        }
        generated_pdf = PublicPDF(
            title = 'PDF file title',
            extra_text = 'Any associated text you might need (optional)',
            **kwargs,
        )
        generated_pdf.save()

**Private generated PDF** ::

    from django_simple_file_handler.models import PrivatePDF

    class MyModel(models.Model):
        ...
        kwargs = {
            'template_location' : 'path/to/your/html_template.html',
            'data' : {
                'value_one': 'Whatever value you need in your HTML template',
                'value_two': 'Whatever value you need in your HTML template',
                'value_three': 'Whatever value you need in your HTML template',
            },
        }
        generated_pdf = PrivatePDF(
            title = 'PDF file title',
            extra_text = 'Any associated text you might need (optional)',
            **kwargs,
        )
        generated_pdf.save()

The proxy URL would then be accessed at ``generated_pdf.proxy_url``.

**Temporary generated PDF** ::

    from django_simple_file_handler.models import TemporaryPDF

    class MyModel(models.Model):
        ...
        kwargs = {
            'template_location' : 'path/to/your/html_template.html',
            'data' : {
                'value_one': 'First value in your HTML template',
                'value_two': 'Second value in your HTML template',
                'value_three': 'Third value in your HTML template',
            },
        }
        generated_pdf = TemporaryPDF(
            title = 'PDF file title',
            extra_text = 'Any associated text you might need (optional)',
            **kwargs,
        )
        generated_pdf.save()

----------
File types
----------

Supported document formats include PDF, ZIP, Word, Excel and PowerPoint. Supported image formats include PNG, JPEG, GIF and TIFF (source for processed images only). Some generic MIME types have been included due to limitations of libmagic in identifying Microsoft Office file formats.

To support different file types, initialize your model with your own dictionary of allowed attributes: ::

    ...
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._meta.get_field('saved_file').validators = [
                CheckExtMIME(allowed_attributes=MY_DICTIONARY),
            ]

The dictionary's format can optionally include arguments for file extensions, MIME types and verbose names for file formats (these will appear in error messages if given). Here is an example: ::

    MY_DICTIONARY = {
        'allowed_extensions' : [
            'abc',
            'def',
            'ghi',
        ],
        'allowed_mimetypes' : [
            'application/example1',
            'application/example2',
            'image/example3',
        ],
        'allowed_verbose' : [
            'Format name 1',
            'Format name 2',
            'Format name 3',
        ],
    }

----------------
Image attributes
----------------

By default, images are processed into PNG format with RGB data. To use something else, subclass the ProcessedImage model and change the attributes as in this example: ::

    from django_simple_file_handler.models import ProcessedImage

    ...
    class MyProcessedImage(ProcessedImage):
        output_mode = 'P'
        content_type = 'image/gif'
        file_format = 'GIF'
        file_extension = 'gif'

--------------
File locations
--------------

If you wish to change the locations where documents, images or generated PDFs are stored, subclass the relevant model and change the attribute as in this example: ::

    from django_simple_file_handler import ProcessedImage

    ...
    class MyProcessedImage(ProcessedImage):
        subdirectory_path = 'path/to/save/location/'

------------
Advanced use
------------

The django-simple-file-handler models are assembled from reusable mixins and functions that can of course, imported for use with your own code.