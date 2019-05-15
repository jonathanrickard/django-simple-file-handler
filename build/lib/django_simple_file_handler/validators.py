from mimetypes import (
    guess_type,
)
from os.path import (
    splitext,
)


from django.core.exceptions import (
    ValidationError,
)
from django.utils.deconstruct import (
    deconstructible,
)


def formatted_list(unformatted_list):
    return ''.join('{}, ' .format(item) for item in unformatted_list)[:-2]


@deconstructible
class CheckExtMIME:
    def __init__(self, allowed_attributes=None):
        if allowed_attributes is None:
            allowed_attributes = {}
        self.allowed_extensions = allowed_attributes.get('allowed_extensions', [])
        self.allowed_mimetypes = allowed_attributes.get('allowed_mimetypes', [])
        self.allowed_verbose = allowed_attributes.get('allowed_verbose', self.allowed_mimetypes)

    def __call__(self, value):
        ext = splitext(value.name)[1][1:].lower()
        ''' Check file extension '''
        if self.allowed_extensions and ext not in self.allowed_extensions:
            error_message = 'Allowed file extensions: {}.' .format(formatted_list(self.allowed_extensions))
            raise ValidationError(error_message)
        ''' Check file MIME type '''
        try:
            from magic import from_buffer
            mimetype = from_buffer(value.read(1024), mime=True)
        except ImportError:
            mimetype = guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            error_message = 'Allowed file types: {}.' .format(formatted_list(self.allowed_verbose))
            raise ValidationError(error_message)
