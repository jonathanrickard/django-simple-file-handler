from django.test import (
    TestCase,
)


from ..models import (
    PrivateDocument,
    PrivatePDF,
)
from ..views import *
from .test_functions import (
    create_document_instance,
    create_pdf_instance,
    create_response,
)


class MixinWrap:
    class BaseMixin(TestCase):
        def setUp(self):
            self.response = create_response(self)
        def test_proxy(self):
            self.assertEqual(self.response.status_code, 200)
            self.assertEqual(self.response.content, self.test_instance.saved_file.read())
        def tearDown(self):
            self.test_instance.delete()


class PrivateDocumentViewTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def setUp(self):
        self.test_instance = create_document_instance(PrivateDocument)
        self.test_view = proxy_document
        self.reverse_name = 'django_simple_file_handler:proxy_document'
        super().setUp()


class PrivatePDFViewTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def setUp(self):
        self.test_instance = create_pdf_instance(PrivatePDF)
        self.test_view = proxy_pdf
        self.reverse_name = 'django_simple_file_handler:proxy_pdf'
        super().setUp()
