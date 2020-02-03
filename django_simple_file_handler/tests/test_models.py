from PIL import (
    Image,
)


from django.test import (
    TestCase,
)


from ..models import (
    PrivateDocument,
    PrivatePDF,
    ProcessedImage,
    PublicDocument,
    PublicPDF,
    TemporaryDocument,
    TemporaryPDF,
    UnprocessedImage,
)
from .functions import (
    attribute_exists,
    create_document_instance,
    create_pdf_instance,
    create_processed_image_instance,
    create_unprocessed_image_instance,
    custom_subdirectory,
    pillow_settings,
)


class MixinWrap:
    class BaseMixin(TestCase):
        checked_attributes = [
            'created',
            'updated',
        ]
        longMessage = False

        def test_file_exists(self):
            error_msg = "For '{}', the file does not exist".format(
                self.test_instance.__class__.__name__,
            )
            self.assertIs(attribute_exists(self.test_instance.saved_file.file), True, error_msg)

        def test_attribute_has_value(self):
            for attr in self.checked_attributes:
                error_msg = "For '{}', the attribute '{}' did not return a value".format(
                    self.test_instance.__class__.__name__,
                    attr,
                )
                self.assertTrue(len(str(getattr(self.test_instance, attr))) > 0, error_msg)

        def test_attribute_value(self):
            try:
                checked_values = self.checked_values
            except AttributeError:
                checked_values = {}
            for attr, value in checked_values.items():
                error_msg = "For '{}', the value for '{}' was not '{}'".format(
                    self.test_instance.__class__.__name__,
                    attr,
                    value,
                )
                self.assertTrue(getattr(self.test_instance, attr, '') == value, error_msg)

        def test_attribute_value_contains(self):
            try:
                checked_values_contain = self.checked_values_contain
            except AttributeError:
                checked_values_contain = {}
            for attr, value in checked_values_contain.items():
                error_msg = "For '{}', the value for '{}' did not contain '{}'".format(
                    self.test_instance.__class__.__name__,
                    attr,
                    value,
                )
                self.assertIn(value, str(getattr(self.test_instance, attr, '')), error_msg)

        def tearDown(self):
            self.test_instance.delete()


class PublicDocumentTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_values = {
            'title': 'Test Document',
            'extra_text': 'Test extra text',
            'generated_name': 'test-document',
            'saved_file': custom_subdirectory('documents/public/test-document.pdf'),
        }

    def setUp(self):
        self.test_instance = create_document_instance(PublicDocument)


class PrivateDocumentTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_attributes += [
            'generated_name',
        ]
        self.checked_values = {
            'title': 'Test Document',
            'extra_text': 'Test extra text',
            'proxy_slug': 'test-document.pdf',
        }
        self.checked_values_contain = {
            'saved_file': custom_subdirectory('documents/private/'),
        }

    def setUp(self):
        self.test_instance = create_document_instance(PrivateDocument)


class TemporaryDocumentTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_values = {
            'title': 'Test Document',
            'extra_text': 'Test extra text',
        }
        self.checked_values_contain = {
            'generated_name': 'test-document',
            'saved_file': custom_subdirectory('documents/temporary/'),
        }

    def setUp(self):
        self.test_instance = create_document_instance(TemporaryDocument)


class UnprocessedImageTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_values = {
            'title': 'Test Image',
            'extra_text': 'Test extra text',
            'generated_name': 'test-image',
            'saved_file': custom_subdirectory('images/unprocessed/test-image.jpeg'),
        }

    def setUp(self):
        self.test_instance = create_unprocessed_image_instance(UnprocessedImage)


class ProcessedImageTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_attributes += [
            'generated_name',
        ]
        self.checked_values_contain = {
            'saved_file': custom_subdirectory('images/raw/'),
        }

    def setUp(self):
        self.test_instance = create_processed_image_instance(ProcessedImage)

    def test_processed_image_processed_file(self):
        processed_image = self.test_instance.processed_file
        output_mode = pillow_settings().get('output_mode', 'RGB')
        file_format = pillow_settings().get('file_format', 'PNG')
        file_extension = pillow_settings().get('file_format', 'png')
        self.assertIn(custom_subdirectory('images/processed'), processed_image.name)
        self.assertIn(file_extension, processed_image.name)
        processed_file = Image.open(processed_image.file)
        self.assertIs(processed_file.width, 200)
        self.assertIs(processed_file.height, 100)
        self.assertIs(processed_file.mode, output_mode)
        self.assertIs(processed_file.format, file_format)


class PublicPDFTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_values = {
            'title': 'PDF file name',
            'extra_text': 'Test extra text',
            'generated_name': 'pdf-file-name',
            'saved_file': custom_subdirectory('pdf/public/pdf-file-name.pdf'),
        }

    def setUp(self):
        self.test_instance = create_pdf_instance(PublicPDF)


class PrivatePDFTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_attributes += [
            'generated_name',
        ]
        self.checked_values = {
            'title': 'PDF file name',
            'extra_text': 'Test extra text',
            'proxy_slug': 'pdf-file-name.pdf',
        }
        self.checked_values_contain = {
            'saved_file': custom_subdirectory('pdf/private/'),
        }

    def setUp(self):
        self.test_instance = create_pdf_instance(PrivatePDF)


class TemporaryPDFTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked_values = {
            'title': 'PDF file name',
            'extra_text': 'Test extra text',
        }
        self.checked_values_contain = {
            'generated_name': 'pdf-file-name',
            'saved_file': custom_subdirectory('pdf/temporary/'),
        }

    def setUp(self):
        self.test_instance = create_pdf_instance(TemporaryPDF)
