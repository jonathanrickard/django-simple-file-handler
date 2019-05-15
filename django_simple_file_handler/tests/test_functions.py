from io import (
    BytesIO,
)


from PIL import (
    Image,
)


from django.conf import (
    settings,
)
from django.contrib.auth.models import (
    User,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.test import (
    RequestFactory,
)
from django.urls import (
    reverse,
)


def custom_subdirectory():
    if hasattr(settings, 'FILE_HANDLER_DIRECTORY'):
        return settings.FILE_HANDLER_DIRECTORY
    else:
        return ''


def pillow_settings():
    if hasattr(settings, 'FILE_HANDLER_PILLOW'):
        return settings.FILE_HANDLER_PILLOW
    else:
        return {}


def create_image_file():
    temp_handle = BytesIO()
    image_file = Image.new(
        'RGB',
        (72, 72),
        (0, 0, 255),
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
        title='Test Document',
        extra_text='Test extra text',
        saved_file=SimpleUploadedFile(
            'test_file.pdf',
            'test file content'.encode(),
            'application/pdf',
        ),
    )
    document_instance.save()
    return document_instance


def create_unprocessed_image_instance(model_name):
    image_instance = model_name(
        title='Test Image',
        extra_text='Test extra text',
        saved_file=create_image_file(),
    )
    image_instance.save()
    return image_instance


def create_processed_image_instance(model_name):
    image_instance = model_name(
        extra_text='Test extra text',
        output_width=200,
        output_height=100,
        saved_file=create_image_file(),
    )
    image_instance.save()
    return image_instance


def create_pdf_instance(model_name):
    pdf_instance = model_name(
        title='PDF file name',
        extra_text='Test extra text',
        template_location='django_simple_file_handler/tests/pdf_test.html',
        template_data={
            'title_name': 'Title of PDF',
            'test_value': 'A test value string',
        },
    )
    pdf_instance.save()
    return pdf_instance


def create_response(self):
    request = RequestFactory().get(reverse(
        self.reverse_name,
        kwargs={
            'proxy_slug': self.test_instance.proxy_slug,
        },
    ))
    request.user = create_user()
    return self.test_view(request, self.test_instance.proxy_slug)


def attribute_exists(instance_attribute):
    return instance_attribute is not None
