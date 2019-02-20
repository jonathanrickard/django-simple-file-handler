from mimetypes import (
    guess_type,
)


from django.contrib.auth.decorators import (
    login_required,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.http import (
    Http404,
    HttpResponse,
)


from .models import (
    PrivateDocument,
    PrivatePDF,
)


@login_required
def proxy_document(request, proxy_slug):
    try:
        private_document = PrivateDocument.objects.get(proxy_slug=proxy_slug)
    except ObjectDoesNotExist:
        raise Http404()
    private_file = private_document.saved_file
    mimetype = guess_type(private_file.name)[0]
    return HttpResponse(
        private_file.read(),
        content_type=mimetype,
    )


@login_required
def proxy_pdf(request, proxy_slug):
    try:
        private_document = PrivatePDF.objects.get(proxy_slug=proxy_slug)
    except ObjectDoesNotExist:
        raise Http404()
    private_file = private_document.saved_file
    mimetype = guess_type(private_file.name)[0]
    return HttpResponse(
        private_file.read(),
        content_type=mimetype,
    )
