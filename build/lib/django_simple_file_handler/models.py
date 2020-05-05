from io import (
    BytesIO,
)
import os
from random import (
    choice,
)
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
)


from django.conf import (
    settings,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.core.files.base import (
    ContentFile,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.db import (
    models,
)
from django.template.loader import (
    get_template,
)
from django.urls import (
    reverse,
)
from django.utils.safestring import (
    mark_safe,
)
from django.utils.text import (
    slugify,
)


from PIL import (
    Image,
)
from xhtml2pdf import (
    pisa,
)
from xhtml2pdf.config.httpconfig import (
    httpConfig,
)


httpConfig.save_keys(
    'nosslcheck',
    True,
)


def create_file_path(instance, filename):
    subdirectory = instance.subdirectory_path
    file_base = instance.generated_name
    file_extension = filename.rsplit('.', 1)[1]
    return '{}{}.{}'.format(subdirectory, file_base, file_extension)


class BaseMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        'last updated',
        auto_now=True,
    )
    generated_name = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    extra_text = models.TextField(
        'extra text (optional)',
        blank=True,
    )
    saved_file = models.FileField(
        'uploaded file',
        upload_to=create_file_path,
        validators=[],
        max_length=254,
    )

    def file_url(self):
        if self.saved_file:
            return self.saved_file.url
        else:
            return 'No file'
    file_url.short_description = 'file URL'

    def file_link(self):
        if self.saved_file:
            return mark_safe(
                '<a href="{}" target="_blank">File link</a>'.format(
                    self.file_url(),
                )
            )
        else:
            return 'No file'
    file_link.short_description = 'file link'
    check_fields = [
        'saved_file',
    ]

    def get_saved_object(self):
        try:
            saved_object = self.__class__.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            saved_object = None
        return saved_object

    def save(self, *args, **kwargs):
        saved_object = self.get_saved_object()
        self.file_deleted = False
        if saved_object is not None:
            for field in self.check_fields:
                if getattr(self, field) != getattr(saved_object, field):
                    getattr(saved_object, field).delete(False)
                    self.file_deleted = True
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ImageMixin(BaseMixin):
    def saved_file_dimesions(self):
        image = Image.open(self.saved_file)
        return image.size

    def saved_file_height(self):
        width, height = self.saved_file_dimesions()
        return height

    def saved_file_width(self):
        width, height = self.saved_file_dimesions()
        return width

    class Meta:
        abstract = True


def create_file(file_name, content_type, temp_handle):
    temp_handle.seek(0)
    processed_file = SimpleUploadedFile(
        file_name,
        temp_handle.read(),
        content_type,
    )
    return processed_file


def link_callback(url, rel):
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT
    if url.startswith(media_url) and media_root is not None:
        path = os.path.join(media_root, url.replace(media_url, ''))
    elif url.startswith(static_url) and static_root is not None:
        path = os.path.join(static_root, url.replace(static_url, ''))
    else:
        return url
    return path


def create_pdf(generated_name, template_location, template_data):
    template = get_template(template_location)
    rendered_html = template.render(template_data)
    temp_handle = BytesIO()
    base_name = generated_name
    file_extension = 'pdf'
    file_name = '{}.{}'.format(base_name, file_extension)
    content_type = 'application/pdf'
    try:
        if settings.FILE_HANDLER_WEASYPRINT:
            from weasyprint import HTML
            HTML(string=rendered_html).write_pdf(target=temp_handle)
    except AttributeError:
        pisa.CreatePDF(
            rendered_html,
            dest=temp_handle,
            link_callback=link_callback,
        )
    return create_file(file_name, content_type, temp_handle)


class PDFMixin(models.Model):
    def __init__(self, *args, **kwargs):
        self.template_data = kwargs.pop('template_data', {})
        super().__init__(*args, **kwargs)

    template_location = models.TextField(
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.template_data:
            self.saved_file.delete(False)
            self.saved_file = create_pdf(
                self.generated_name,
                self.template_location,
                self.template_data,
            )
            self.template_data = {}
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TitledMixin(models.Model):
    title = models.CharField(
        max_length=245,
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


def create_slug(title):
    return slugify(title)


class PublicMixin(models.Model):
    def save(self, *args, **kwargs):
        self.generated_name = create_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def create_key(length):
    return ''.join(choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(length))


def create_proxy(self):
    slug = create_slug(self.title)
    file_extension = self.saved_file.url.rsplit('.', 1)[1]
    return '{}.{}'.format(slug, file_extension)


class PrivateMixin(models.Model):
    proxy_slug = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )

    def proxy_url(self):
        if self.proxy_slug:
            return reverse(
                self.proxy_reverse,
                kwargs={
                    'proxy_slug': self.proxy_slug
                },
            )
        else:
            return 'No file'
    proxy_url.short_description = 'proxy URL'

    def proxy_link(self):
        if self.saved_file:
            return mark_safe(
                '<a href="{}" target="_blank">Proxy link</a>'.format(
                    self.proxy_url(),
                )
            )
        else:
            return 'No file'
    proxy_link.short_description = 'proxy link'

    def save(self, *args, **kwargs):
        if not self.generated_name:
            self.generated_name = create_key(128)
        self.proxy_slug = create_proxy(self)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def create_slug_with_key(title):
    slug = create_slug(title)
    key = create_key(16)
    return '{}-{}'.format(slug, key)


class TemporaryMixin(models.Model):
    def save(self, *args, **kwargs):
        saved_object = self.get_saved_object()
        if saved_object is not None:
            if self.title != saved_object.title:
                self.generated_name = create_slug_with_key(self.title)
        else:
            self.generated_name = create_slug_with_key(self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class RenameMixin(models.Model):
    def save(self, *args, **kwargs):
        saved_object = self.get_saved_object()
        if saved_object is not None:
            if self.generated_name != saved_object.generated_name:
                if not self.file_deleted:
                    old_file = saved_object.saved_file
                    new_file = ContentFile(old_file.read())
                    new_file.name = old_file.name
                    old_file.delete(False)
                    self.saved_file = new_file
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def custom_subdirectory(path):
    try:
        directory = settings.FILE_HANDLER_DIRECTORY
    except AttributeError:
        directory = ''
    return '{}{}'.format(
        directory,
        path,
    )


class PublicDocument(BaseMixin, TitledMixin, PublicMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    subdirectory_path = custom_subdirectory('documents/public/')

    class Meta:
        verbose_name = 'document (public)'
        verbose_name_plural = 'documents (public)'


class PrivateDocument(BaseMixin, TitledMixin, PrivateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    subdirectory_path = custom_subdirectory('documents/private/')
    proxy_reverse = 'django_simple_file_handler:proxy_document'

    class Meta:
        verbose_name = 'document (private)'
        verbose_name_plural = 'documents (private)'


class TemporaryDocument(BaseMixin, TitledMixin, TemporaryMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = models.CharField(
        max_length=245,
    )
    subdirectory_path = custom_subdirectory('documents/temporary/')

    class Meta:
        verbose_name = 'document (temporary)'
        verbose_name_plural = 'documents (temporary)'


class UnprocessedImage(ImageMixin, TitledMixin, PublicMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    subdirectory_path = custom_subdirectory('images/unprocessed/')

    class Meta:
        verbose_name = 'image (unprocessed)'
        verbose_name_plural = 'images (unprocessed)'


def create_image_path(instance, filename):
    subdirectory = instance.image_path
    return '{}{}'.format(subdirectory, filename)


def process_image(instance, output_mode, content_type, file_format, file_extension):
    input_image = Image.open(instance.saved_file)
    output_width = instance.output_width
    output_height = instance.output_height
    temp_handle = BytesIO()
    file_name = '{}.{}'.format(instance.generated_name, file_extension)
    ''' Convert the mode if necessary '''
    if input_image.mode is not output_mode:
        image = input_image.convert(output_mode)
    else:
        image = input_image
    ''' Resize the image '''
    input_width, input_height = image.size
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
    ''' Crop the image if necessary '''
    cropped_image = resized_image.crop(
        (
            0,
            0,
            output_width,
            output_height
        )
    )
    ''' Convert the file format if necessary '''
    cropped_image.save(
        temp_handle,
        file_format,
    )
    return create_file(file_name, content_type, temp_handle)


def pillow_settings():
    try:
        return settings.FILE_HANDLER_PILLOW
    except AttributeError:
        return {}


class ProcessedImage(ImageMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    output_width = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    output_height = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    processed_file = models.FileField(
        upload_to=create_image_path,
        blank=True,
        null=True,
    )
    subdirectory_path = custom_subdirectory('images/raw/')
    image_path = custom_subdirectory('images/processed/')
    output_mode = pillow_settings().get('output_mode', 'RGB')
    content_type = pillow_settings().get('content_type', 'image/png')
    file_format = pillow_settings().get('file_format', 'PNG')
    file_extension = pillow_settings().get('file_format', 'png')
    check_fields = [
        'saved_file',
        'processed_file',
    ]

    def image_dimesions(self):
        image = Image.open(self.processed_file)
        return image.size

    def image_height(self):
        width, height = self.image_dimesions()
        return height

    def image_width(self):
        width, height = self.image_dimesions()
        return width

    def image_url(self):
        if self.saved_file:
            return self.processed_file.url
        else:
            return 'No file'

    def image_link(self):
        if self.saved_file:
            return mark_safe(
                '<a href="{}" target="_blank">Image link</a>'.format(
                    self.image_url(),
                )
            )
        else:
            return 'No file'
    image_link.short_description = 'image link'

    def save(self, *args, **kwargs):
        image_args = [
            self,
            self.output_mode,
            self.content_type,
            self.file_format,
            self.file_extension,
        ]
        saved_object = self.get_saved_object()
        if saved_object is not None:
            changeable_fields = [
                'saved_file',
                'output_width',
                'output_height',
            ]
            for field in changeable_fields:
                if getattr(self, field) != getattr(saved_object, field):
                    self.processed_file = process_image(*image_args)
                    break
        else:
            self.generated_name = create_key(length=32)
            self.processed_file = process_image(*image_args)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'image (processed)'
        verbose_name_plural = 'images (processed)'


class PublicPDF(BaseMixin, PDFMixin, TitledMixin, PublicMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    subdirectory_path = custom_subdirectory('pdf/public/')

    class Meta:
        verbose_name = 'PDF (public)'
        verbose_name_plural = 'PDFs (public)'


class PrivatePDF(BaseMixin, PDFMixin, TitledMixin, PrivateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    subdirectory_path = custom_subdirectory('pdf/private/')
    proxy_reverse = 'django_simple_file_handler:proxy_pdf'

    class Meta:
        verbose_name = 'PDF (private)'
        verbose_name_plural = 'PDFs (private)'


class TemporaryPDF(BaseMixin, PDFMixin, TitledMixin, TemporaryMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = models.CharField(
        max_length=245,
    )
    subdirectory_path = custom_subdirectory('pdf/temporary/')

    class Meta:
        verbose_name = 'PDF (temporary)'
        verbose_name_plural = 'PDFs (temporary)'
