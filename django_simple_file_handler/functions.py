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
    subdirectory = instance.subdirectory_path
    file_base = instance.generated_name
    file_extension = splitext(filename)[1][1:].lower()
    return '{}{}.{}' .format(subdirectory, file_base, file_extension)


def create_image_path(instance, filename):
    subdirectory = instance.image_path
    return '{}{}' .format(subdirectory, filename)


def create_key(length):
    return ''.join(choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(length))

    
def create_slug(title):
    return slugify(title)


def create_slug_with_key(title):
    slug = create_slug(title)
    key = create_key(16)
    return '{}-{}' .format(slug, key)


def create_proxy(self):
    slug = create_slug(self.title)
    file_extension = splitext(basename(self.saved_file.path))[1][1:]
    return '{}.{}' .format(slug, file_extension)


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
    file_name = '{}.{}' .format(instance.generated_name, file_extension)
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


def create_pdf(generated_name, template_location, template_data):
    template = get_template(template_location)
    rendered_html  = template.render(template_data)
    temp_handle = BytesIO()
    base_name = generated_name
    file_extension = 'pdf'
    file_name = '{}.{}' .format(base_name, file_extension)
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
