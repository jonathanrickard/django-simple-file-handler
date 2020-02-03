from django.test import (
    TestCase,
)


from ..models import (
    PrivateDocument,
    PrivatePDF,
)
from ..views import (
    proxy_document,
    proxy_pdf,
)
from .functions import (
    create_document_instance,
    create_pdf_instance,
    create_response,
    file_equals,
    status_code_equals,
)


class MixinWrap:
    class BaseMixin(TestCase):
        longMessage = False

        def setUp(self):
            self.response = create_response(self)

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

    def test_get(self):
        status_code_equals(self, 'proxy_document', 200)

    def test_file(self):
        file_equals(self, 'proxy_document')


class PrivatePDFViewTests(MixinWrap.BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.test_instance = create_pdf_instance(PrivatePDF)
        self.test_view = proxy_pdf
        self.reverse_name = 'django_simple_file_handler:proxy_pdf'
        super().setUp()

    def test_get(self):
        status_code_equals(self, 'proxy_pdf', 200)

    def test_file(self):
        file_equals(self, 'proxy_pdf')
