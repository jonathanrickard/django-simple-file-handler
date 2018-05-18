from io import (
    BytesIO,
)


from PIL import (
    Image,
)


from django.contrib.auth.models import (
    User,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)


def create_image_file():
    temp_handle = BytesIO()
    image_file = Image.new(
        'RGB',
        (72,72),
        (0,0,255),
    )
    image_file.save(
        temp_handle,
        'jpeg',
    )
    temp_handle.seek(0)
    return SimpleUploadedFile(
        'test_image.jpeg',
        temp_handle.read(),
        'image/jpeg',
    )


def create_user():
    user = User.objects.create_user(
        username='test_user',
        password='test_password',
    )
    return user


def create_document_instance(model_name):
    document_instance = model_name(
        title = 'Test Document',
        extra_text = 'Test extra text',
        saved_file = SimpleUploadedFile(
            'test_file.pdf',
            'test file content'.encode(),
            'application/pdf',
        ),

    )
    document_instance.save()
    return document_instance


def create_unprocessed_image_instance(model_name):
    image_instance = model_name(
        title = 'Test Image',
        extra_text = 'Test extra text',
        saved_file = create_image_file(),
    )
    image_instance.save()
    return image_instance


def create_processed_image_instance(model_name):
    image_instance = model_name(
        extra_text = 'Test extra text',
        output_width = 200,
        output_height = 100,
        saved_file = create_image_file(),
    )
    image_instance.save()
    return image_instance


def create_pdf_instance(model_name):
    kwargs = {
        'template_location' : 'django_simple_file_handler/tests/pdf_test.html',
        'data' : {
            'title_name': 'Title of PDF',
            'test_value': 'A test value string',
        },
    }
    pdf_instance = model_name(
        title = 'PDF file name',
        extra_text = 'Test extra text',
        **kwargs,
    )
    pdf_instance.save()
    return pdf_instance


def attribute_exists(instance_attribute):
    return instance_attribute is not None
