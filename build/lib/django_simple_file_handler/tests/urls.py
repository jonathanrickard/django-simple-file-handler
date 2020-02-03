from django.urls import (
    include,
    path,
)


urlpatterns = [
    path(
        'file_test/',
        include('django_simple_file_handler.urls'),
    ),
]
