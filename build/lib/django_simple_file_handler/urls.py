from django.conf.urls import (
    url,
)


from .views import *


app_name = 'django_simple_file_handler'


urlpatterns = [
	url(
	    r'^documents/(?P<proxy_slug>.*)',
	    proxy_document,
	    name='proxy_document',
	),
	url(
	    r'^pdf/(?P<proxy_slug>.*)',
	    proxy_pdf,
	    name='proxy_pdf',
	),
]
