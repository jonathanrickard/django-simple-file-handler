from django.apps import (
    AppConfig,
)


class Config(AppConfig):
    name = 'django_simple_file_handler'
    verbose_name = 'Files and images'

    def ready(self):
        from .signals import (
            handlers,
        )
