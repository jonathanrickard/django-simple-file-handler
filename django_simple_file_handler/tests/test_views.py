from django.urls import (
    reverse,
)
from django.test import (
    RequestFactory,
    TestCase,
)


from django_simple_file_handler.models import (
    PrivateDocument,
    PrivatePDF,
)
from django_simple_file_handler.views import *


from .functions import (
    create_user,
    create_document_instance,
    create_pdf_instance,
)


class PrivateDocumentViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user()
        self.private_document = create_document_instance(PrivateDocument)
    def test_document_proxy(self):
        request = self.factory.get(reverse(
            'django_simple_file_handler:proxy_document',
            kwargs={
                'proxy_slug': self.private_document.proxy_slug
            },
        ))
        request.user = self.user
        response = proxy_document(request, self.private_document.proxy_slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.private_document.saved_file.read())
    def tearDown(self):
        self.private_document.delete()

class PrivatePDFViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user()
        self.private_pdf = create_pdf_instance(PrivatePDF)
    def test_pdf_proxy(self):
        request = self.factory.get(reverse(
            'django_simple_file_handler:proxy_pdf',
            kwargs={
                'proxy_slug': self.private_pdf.proxy_slug
            },
        ))
        request.user = self.user
        response = proxy_pdf(request, self.private_pdf.proxy_slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.private_pdf.saved_file.read())
    def tearDown(self):
        self.private_pdf.delete()
