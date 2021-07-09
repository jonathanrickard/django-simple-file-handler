==========================
django-simple-file-handler
==========================

The django-simple-file-handler Django app uploads and manages documents and images. It is most useful when used to add these functions to your own apps, and it can also be used to add image processing and PDF generation from HTML templates.

Please note that "private" files and PDFs would be more accurately described as "hidden." The app generates a proxy URL that will load the file for a logged-in user and stores the file with a name consisting of many random characters. Still, it is possible to load these files without logging in if the file path is known.

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
        path(
            'private-file-pseudo-directory-path/',
            include('django_simple_file_handler.urls'),
        ),
    ]

------
Basics
------

Public and private document objects, as well as unprocessed image objects, can be created and managed via the admin site. Other types are read-only in the admin site.

All types can be created and accessed by subclassing or creating a foreign key in your own apps.

Temporary documents and temporary PDFs are intended to be used when two or more objects might need to have the same title. These add a string of random characters to the ends of file names to prevent overwriting files.

**Classes**

* ``PublicDocument`` — Includes uploaded document file
* ``PrivateDocument`` — Includes uploaded document file with a proxy URL requiring login
* ``TemporaryDocument`` —  Includes uploaded document file with a modified file name allowing title duplication
* ``UnprocessedImage`` — Includes uploaded image file
* ``ProcessedImage`` — Includes uploaded image file and processed image file
* ``PublicPDF`` — Includes generated PDF file
* ``PrivatePDF`` — Includes generated PDF file with a proxy URL requiring login
* ``TemporaryPDF`` — Includes generated PDF file with a modified file name allowing title duplication

**Attributes**

* ``created`` — ``DateTimeField`` with automatically generated value
* ``updated`` — ``DateTimeField`` with automatically generated value
* ``title`` — ``CharField`` with ``max_length`` of 245 characters (not available for ``ProcessedImage``)
* ``extra_text`` — ``TextField`` (optional)
* ``saved_file`` — ``FileField`` for the uploaded file
* ``processed_file`` — ``FileField`` for processed image (``ProcessedImage`` only)
* ``output_width`` — ``PositiveIntegerField`` for processed image width in pixels (``ProcessedImage`` only)
* ``output_height`` — ``PositiveIntegerField`` for processed image height in pixels (``ProcessedImage`` only)

**Methods**

* ``file_url`` — Returns URL of the uploaded file as a string
* ``file_link`` — Returns an HTML link to the URL of the uploaded file as a string
* ``proxy_url`` — Returns proxy URL for the uploaded file as a string (``PrivateDocument`` and ``PrivatePDF`` only)
* ``proxy_link`` — Returns an HTML link to the proxy URL for the uploaded file as a string (``PrivateDocument`` and ``PrivatePDF`` only)
* ``image_url`` — Returns URL of the processed image file as a string (``ProcessedImage`` only)
* ``image_link`` — Returns  an HTML link to the URL of the processed image file as a string (``ProcessedImage`` only)
* ``image_height`` — Returns an integer for the height of the processed image in pixels. (``ProcessedImage`` only)
* ``image_width`` — Returns an integer for the width of the processed image in pixels. (``ProcessedImage`` only)
* ``saved_file_height`` — Returns an integer for the height of the source image in pixels. (``ProcessedImage`` only)
* ``saved_file_width`` — Returns an integer for the width of the source image in pixels. (``ProcessedImage`` only)

----------------
Processed images
----------------

Refer to the `Pillow <https://github.com/python-pillow/Pillow>`_ documentation for allowed import formats or see the section below on file types to limit them in your forms.

Images are processed when an instance is saved with a file assigned to the ``saved_file`` field and a value for one or both of the ``output_width`` and ``output_height`` fields. If one value is given, the image will be scaled proportionally. If both are supplied and they do not match the proportions of the source image, the image will be scaled and cropped on either the bottom or right side, depending on whether the source image is horizontal or vertical.

The processed image is stored in the ``processed_file`` field, while the original file assigned to ``saved_file`` is unchanged and can be processed again as needed. Refer to the attributes and methods list above for additional information.

By default, images are processed into PNGs with RGBA mode. To change one or more of the output parameters, add a ``FILE_HANDLER_PILLOW`` setting with a dictionary containing parameters you wish to change, as in this example: ::

    FILE_HANDLER_PILLOW = {
        'output_mode': 'P',
        'content_type': 'image/gif',
        'file_format': 'GIF',
        'file_extension': 'gif',
    }

Refer to Pillow documentation for options for these parameters.

---------------
Generating PDFs
---------------

PDF generation will use `WeasyPrint <https://weasyprint.org/>`_ if it is installed and ``FILE_HANDLER_WEASYPRINT = True`` is present in Django settings. Otherwise, it will use `xhtml2pdf <https://github.com/xhtml2pdf/xhtml2pdf>`_, which wil be installed if not present. This app has been tested with WeasyPrint 0.28. Please refer to xhtml2pdf or WeasyPrint documentation for HTML template-formatting specifics.

The example code below uses ``PublicPDF``, but ``PrivatePDF`` and ``TemporaryPDF`` work the same way. ::

    generated_pdf = PublicPDF.objects.create(
        title='title of the generated PDF document',
        extra_text='any additional text needed with the object',
        template_location='path/to/your/html/template.html',
        template_data={
            'value_one': value_to_be_inserted_in_template,
            'value_two': value_to_be_inserted_in_template,
            'value_three': value_to_be_inserted_in_template,
        },
    )

Database object attributes can then be changed without rewriting the PDF file. The file is only written when the ``template_data`` dictionary is given and the object is resaved.

------------
File formats
------------

If `python-magic <https://github.com/ahupp/python-magic>`_ is installed, django-simple-file-handler will use it to check uploaded file MIME types. Otherwise, it will use Python's built-in library. This package has been tested with python-magic 0.4.

Supported document formats include PDF, ZIP, Word, Excel and PowerPoint. Supported unprocessed image formats include PNG, JPEG and GIF.

To support different file types, follow this example for your form: ::

    class MyForm(ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=MY_DICTIONARY))

        class Meta:
            model = PublicDocument
            fields = [
                'title',
                'extra_text',
                'saved_file',
            ]

The dictionary's format can optionally include keys with list values for file extensions, MIME types and verbose names for file formats (these will appear in error messages if given). Here is an example: ::

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
            'Format1',
            'Format2',
            'Format3',
        ],
    }

Dictionaries included in ``django_simple_file_handler.file_types`` include:

* ``CHECK_DOC`` — Allows ZIP, Word, Excel and PowerPoint.
* ``CHECK_WEB_IMAGE`` — Allows GIF, JPEG and PNG.
* ``CHECK_RAW_IMAGE`` — Allows GIF, JPEG, PNG and TIFF.
* ``CHECK_PDF`` — Allows PDF only.
* ``CHECK_ALL_WEB`` — Allows GIF, JPEG, PNG ZIP, Word, Excel and PowerPoint.

--------------
File locations
--------------

By default, images will be stored in your ``media`` directory in subdirectories named ``documents``, ``images`` and ``pdf``. If you wish to change the directory where these subdirectories are created, add ``FILE_HANDLER_DIRECTORY = 'path/to/location/'`` to your settings.

------------
Advanced use
------------

The django-simple-file-handler models and admin classes make use of modular, reusable mixins and functions that can, of course, be imported for use with your own code.
