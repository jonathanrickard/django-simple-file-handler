from PIL import (
    Image,
)


from django.test import (
    TestCase,
)


from django_simple_file_handler.models import *


from .functions import (
    attribute_exists,
    create_document_instance,
    create_processed_image_instance,
    create_unprocessed_image_instance,
    create_pdf_instance,
)


class PublicDocumentTests(TestCase):
    def setUp(self):
        self.document_instance = create_document_instance(PublicDocument)
    def test_public_document_created(self):
        self.assertIs(attribute_exists(self.document_instance.created), True)
    def test_public_document_updated(self):
        self.assertIs(attribute_exists(self.document_instance.updated), True)
    def test_public_document_title(self):
        self.assertIs(attribute_exists(self.document_instance.title), True)
    def test_public_document_generated_name(self):
        self.assertIs(attribute_exists(self.document_instance.generated_name), True)
    def test_public_document_extra_text(self):
        self.assertIs(attribute_exists(self.document_instance.extra_text), True)
    def test_public_document_file_saved(self):
        self.assertIs(attribute_exists(self.document_instance.saved_file.file), True)
    def tearDown(self):
        self.document_instance.delete()


class PrivateDocumentTests(TestCase):
    def setUp(self):
        self.document_instance = create_document_instance(PrivateDocument)
    def test_private_document_created(self):
        self.assertIs(attribute_exists(self.document_instance.created), True)
    def test_private_document_updated(self):
        self.assertIs(attribute_exists(self.document_instance.updated), True)
    def test_private_document_title(self):
        self.assertIs(attribute_exists(self.document_instance.title), True)
    def test_private_document_generated_name(self):
        self.assertIs(attribute_exists(self.document_instance.generated_name), True)
    def test_private_document_extra_text(self):
        self.assertIs(attribute_exists(self.document_instance.extra_text), True)
    def test_private_document_proxy_slug(self):
        self.assertIs(attribute_exists(self.document_instance.proxy_slug), True)
    def test_private_document_file_saved(self):
        self.assertIs(attribute_exists(self.document_instance.saved_file.file), True)
    def tearDown(self):
        self.document_instance.delete()


class TemporaryDocumentTests(TestCase):
    def setUp(self):
        self.document_instance = create_document_instance(TemporaryDocument)
    def test_temporary_document_created(self):
        self.assertIs(attribute_exists(self.document_instance.created), True)
    def test_temporary_document_updated(self):
        self.assertIs(attribute_exists(self.document_instance.updated), True)
    def test_temporary_document_title(self):
        self.assertIs(attribute_exists(self.document_instance.title), True)
    def test_temporary_document_generated_name(self):
        self.assertIs(attribute_exists(self.document_instance.generated_name), True)
    def test_temporary_document_extra_text(self):
        self.assertIs(attribute_exists(self.document_instance.extra_text), True)
    def test_temporary_document_file_saved(self):
        self.assertIs(attribute_exists(self.document_instance.saved_file.file), True)
    def tearDown(self):
        self.document_instance.delete()


class UnprocessedImageTests(TestCase):
    def setUp(self):
        self.image_instance = create_unprocessed_image_instance(UnprocessedImage)
    def test_unprocessed_image_created(self):
        self.assertIs(attribute_exists(self.image_instance.created), True)
    def test_unprocessed_image_updated(self):
        self.assertIs(attribute_exists(self.image_instance.updated), True)
    def test_unprocessed_image_title(self):
        self.assertIs(attribute_exists(self.image_instance.title), True)
    def test_unprocessed_image_generated_name(self):
        self.assertIs(attribute_exists(self.image_instance.generated_name), True)
    def test_unprocessed_image_extra_text(self):
        self.assertIs(attribute_exists(self.image_instance.extra_text), True)
    def test_unprocessed_image_file_saved(self):
        self.assertIs(attribute_exists(self.image_instance.saved_file.file), True)
    def tearDown(self):
        self.image_instance.delete()


class ProcessedImageTests(TestCase):
    def setUp(self):
        self.image_instance = create_processed_image_instance(ProcessedImage)        
    def test_processed_image_created(self):
        self.assertIs(attribute_exists(self.image_instance.created), True)
    def test_processed_image_updated(self):
        self.assertIs(attribute_exists(self.image_instance.updated), True)
    def test_processed_image_generated_name(self):
        self.assertIs(attribute_exists(self.image_instance.generated_name), True)
    def test_processed_image_extra_text(self):
        self.assertIs(attribute_exists(self.image_instance.extra_text), True)
    def test_processed_image_raw_file_saved(self):
        self.assertIs(attribute_exists(self.image_instance.saved_file.file), True)
    def test_processed_image_processed_file_saved(self):
        self.assertIs(attribute_exists(self.image_instance.processed_file.file), True)
        processed_image = Image.open(self.image_instance.processed_file.file)
        self.assertIs(processed_image.width, 200)
        self.assertIs(processed_image.height, 100)
        self.assertIs(processed_image.mode, 'RGB')
        self.assertIs(processed_image.format, 'PNG')
    def tearDown(self):
        self.image_instance.delete()


class PublicPDFTests(TestCase):
    def setUp(self):
        self.pdf_instance = create_pdf_instance(PublicPDF)
    def test_public_pdf_created(self):
        self.assertIs(attribute_exists(self.pdf_instance.created), True)
    def test_public_pdf_updated(self):
        self.assertIs(attribute_exists(self.pdf_instance.updated), True)
    def test_public_pdf_title(self):
        self.assertIs(attribute_exists(self.pdf_instance.title), True)
    def test_public_pdf_generated_name(self):
        self.assertIs(attribute_exists(self.pdf_instance.generated_name), True)
    def test_public_pdf_extra_text(self):
        self.assertIs(attribute_exists(self.pdf_instance.extra_text), True)
    def test_public_pdf_file_creation(self):
        self.assertIs(attribute_exists(self.pdf_instance.saved_file.file), True)
    def tearDown(self):
        self.pdf_instance.delete()
    

class PrivatePDFTests(TestCase):
    def setUp(self):
        self.pdf_instance = create_pdf_instance(PrivatePDF)
    def test_private_pdf_created(self):
        self.assertIs(attribute_exists(self.pdf_instance.created), True)
    def test_private_pdf_updated(self):
        self.assertIs(attribute_exists(self.pdf_instance.updated), True)
    def test_private_pdf_title(self):
        self.assertIs(attribute_exists(self.pdf_instance.title), True)
    def test_private_pdf_generated_name(self):
        self.assertIs(attribute_exists(self.pdf_instance.generated_name), True)
    def test_private_pdf_proxy_slug(self):
        self.assertIs(attribute_exists(self.pdf_instance.proxy_slug), True)
    def test_private_pdf_extra_text(self):
        self.assertIs(attribute_exists(self.pdf_instance.extra_text), True)
    def test_private_pdf_file_creation(self):
        self.assertIs(attribute_exists(self.pdf_instance.saved_file.file), True)
    def tearDown(self):
        self.pdf_instance.delete()


class TemporaryPDFTests(TestCase):
    def setUp(self):
        self.pdf_instance = create_pdf_instance(TemporaryPDF)
    def test_temporary_pdf_created(self):
        self.assertIs(attribute_exists(self.pdf_instance.created), True)
    def test_temporary_pdf_updated(self):
        self.assertIs(attribute_exists(self.pdf_instance.updated), True)
    def test_temporary_pdf_title(self):
        self.assertIs(attribute_exists(self.pdf_instance.title), True)
    def test_temporary_pdf_generated_name(self):
        self.assertIs(attribute_exists(self.pdf_instance.generated_name), True)
    def test_temporary_pdf_extra_text(self):
        self.assertIs(attribute_exists(self.pdf_instance.extra_text), True)
    def test_temporary_pdf_file_creation(self):
        self.assertIs(attribute_exists(self.pdf_instance.saved_file.file), True)
    def tearDown(self):
        self.pdf_instance.delete()
