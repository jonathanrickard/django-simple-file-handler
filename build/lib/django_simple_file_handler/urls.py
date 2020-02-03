from django.urls import (
    path,
)


from .views import (
    proxy_document,
    proxy_pdf,
)


app_name = 'django_simple_file_handler'


urlpatterns = [
    path(
        'documents/<proxy_slug>',
        proxy_document,
        name='proxy_document',
    ),
    path(
        'pdf/<proxy_slug>',
        proxy_pdf,
        name='proxy_pdf',
    ),
]
