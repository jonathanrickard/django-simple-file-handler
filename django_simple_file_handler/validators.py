from mimetypes import (
    guess_type,
)
from os.path import (
    join,
    splitext,
)


from django.core.exceptions import (
    ValidationError,
)
from django.utils.deconstruct import (
    deconstructible,
)


def formatted_list(unformatted_list):
    return ''.join('{0}, ' .format(i) for i in unformatted_list)[:-2]


@deconstructible
class CheckExtMIME:
    def __init__(self, allowed_attributes={}):
        self.allowed_extensions = allowed_attributes.get('allowed_extensions', [])
        self.allowed_mimetypes = allowed_attributes.get('allowed_mimetypes', [])
        self.allowed_verbose = allowed_attributes.get('allowed_verbose', self.allowed_mimetypes)
    def __call__(self, value):
        ext = splitext(value.name)[1][1:].lower()                                                                   # Check file extension.
        if self.allowed_extensions and not ext in self.allowed_extensions:
            error_message = 'Allowed file extensions: {0}.' .format(formatted_list(self.allowed_extensions))
            raise ValidationError(error_message)
        try:                                                                                                        # Check file MIME type.
            from magic import from_buffer
            mimetype = from_buffer(value.read(1024), mime=True)
        except ImportError:
            mimetype = guess_type(value.name)[0]
        if self.allowed_mimetypes and not mimetype in self.allowed_mimetypes:
            error_message = 'Allowed file types: {0}.' .format(formatted_list(self.allowed_verbose))
            raise ValidationError(error_message)
