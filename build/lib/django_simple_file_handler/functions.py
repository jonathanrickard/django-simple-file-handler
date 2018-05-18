from io import (
    BytesIO,
)
from os.path import (
    basename,
    join,
    splitext,
)
from random import (
    choice,
)
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
)


from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.template.loader import (
    get_template,
)
from django.utils.text import (
    slugify,
)


def create_file_path(instance, filename):
	path = instance.subdirectory_path
	format = instance.generated_name + '.' + splitext(filename)[1][1:].lower()
	return join(path, format)


def create_key(length):
    return ''.join(choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(length))

    
def create_slug(title):
    return slugify(title)


def create_slug_with_key(title):
    key = create_key(16)
    return slugify(title)[:200] + '-' + key


def create_proxy(self):
    return slugify(self.title)[:200] + '.' + splitext(basename(self.saved_file.path))[1][1:]


def create_file(file_name, content_type, temp_handle):
    temp_handle.seek(0)
    processed_file = SimpleUploadedFile(
        file_name,
        temp_handle.read(),
        content_type,
    )
    return processed_file


def process_image(instance, output_mode, content_type, file_format, file_extension):
    from PIL import Image
    input_image = Image.open(instance.saved_file)
    output_width = instance.output_width
    output_height = instance.output_height
    temp_handle = BytesIO()
    file_name = instance.generated_name + '.' + file_extension
    if input_image.mode is not output_mode:                                 # Convert the mode if necessary.
        image = input_image.convert(output_mode)
    else:
        image = input_image
    input_width, input_height = image.size                                  # Resize the image.
    input_ratio = input_height/input_width
    if not output_height:
        output_height = int(output_width*input_ratio)
    if not output_width:
        output_width = int(output_height/input_ratio)
    output_ratio = output_height/output_width
    if input_ratio >= output_ratio:
        resize_width = output_width
        resize_height = int(resize_width*input_ratio)
    else:
        resize_height = output_height
        resize_width = int(resize_height/input_ratio)
    resized_image = image.resize(
        (
            resize_width,
            resize_height,
        ),
        Image.ANTIALIAS,
    )
    cropped_image = resized_image.crop(                                     # Crop the image if necessary.
        (
            0,
            0,
            output_width,
            output_height
        )
    )
    cropped_image.save(                                                     # Convert the file format if necessary.
        temp_handle,
        file_format,
    )
    return create_file(file_name, content_type, temp_handle)


def create_pdf(generated_name, template_location, data):
    template = get_template(template_location)
    rendered_html  = template.render(data)
    temp_handle = BytesIO()
    file_name = generated_name + '.pdf'
    content_type = 'application/pdf'
    try:
        from weasyprint import HTML
        pdf = HTML(string=rendered_html).write_pdf(target=temp_handle)
    except ImportError:
        try:
            from xhtml2pdf import pisa
            pdf = pisa.CreatePDF(
                rendered_html,
                temp_handle,
            )
        except ImportError:
            pass
    return create_file(file_name, content_type, temp_handle)


def file_compare(instance, fields, **kwargs):
    try:
        saved_object = instance.__class__.objects.get(pk=instance.pk)
        for field in fields:
            if getattr(instance, field) != getattr(saved_object, field):
                getattr(saved_object, field).delete(False)
    except ObjectDoesNotExist:
        pass


def file_delete(instance, fields, **kwargs):
    try:
        for field in fields:
            getattr(instance, field).delete(False)
    except:
        pass
