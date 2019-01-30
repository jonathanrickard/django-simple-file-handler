from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.core.files.base import (
    ContentFile,
)
from django.db import (
    models,
)
from django.urls import (
    reverse,
)


from .dictionaries import *
from .functions import *
from .validators import (
    CheckExtMIME,
)


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
            return '{}' .format(self.saved_file.url)
        else:
            return 'No file'
    file_url.short_description = 'file URL'
    def file_link(self):
        if self.saved_file:
            return '<a href="{}" target="_blank">File link</a>' .format(self.file_url())
        else:
            return 'No file'
    file_link.short_description = 'file link'
    file_link.allow_tags = True
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
        if saved_object is not None:
            for field in self.check_fields:
                if getattr(self, field) != getattr(saved_object, field):
                    getattr(saved_object, field).delete(False)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


class PDFMixin(models.Model):
    def __init__(self, *args, **kwargs):
        self.template_data = kwargs.pop('template_data',{})
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
            self.template_data={}
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


class PublicMixin(models.Model):
    def save(self, *args, **kwargs):
        saved_object = self.get_saved_object()
        if saved_object is not None:
            if self.title != saved_object.title:
                self.generated_name = create_slug(self.title)
        else:
            self.generated_name = create_slug(self.title)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


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
            return '<a href="{}" target="_blank">Proxy link</a>' .format(self.proxy_url())
        else:
            return 'No file'
    proxy_link.short_description = 'proxy link'
    proxy_link.allow_tags = True
    def save(self, *args, **kwargs):
        if not self.generated_name:
            self.generated_name = create_key(128)
        saved_object = self.get_saved_object()
        if saved_object is not None:
            if self.title != saved_object.title:
                self.proxy_slug = create_proxy(self)
        else:
            self.proxy_slug = create_proxy(self)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


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
                try:
                    old_file = saved_object.saved_file
                    new_file = ContentFile(old_file.read())
                    new_file.name = old_file.name
                    old_file.delete(False)
                    self.saved_file = new_file
                except FileNotFoundError:
                    pass
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


class PublicDocument(BaseMixin, TitledMixin, PublicMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_DOC),
        ]
    subdirectory_path = 'documents/public/'
    class Meta:
        verbose_name = 'document (public)'
        verbose_name_plural = 'documents (public)'


class PrivateDocument(BaseMixin, TitledMixin, PrivateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_DOC),
        ]
    subdirectory_path = 'documents/private/'
    proxy_reverse = 'django_simple_file_handler:proxy_document'
    class Meta:
        verbose_name = 'document (private)'
        verbose_name_plural = 'documents (private)'


class TemporaryDocument(BaseMixin, TitledMixin, TemporaryMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_DOC),
        ]
    title = models.CharField(
        max_length=245,
    )
    subdirectory_path = 'documents/temporary/'
    class Meta:
        verbose_name = 'document (temporary)'
        verbose_name_plural = 'documents (temporary)'


class UnprocessedImage(BaseMixin, TitledMixin, PublicMixin, RenameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_WEB_IMAGE),
        ]
    subdirectory_path = 'images/unprocessed/'
    class Meta:
        verbose_name = 'image (unprocessed)'
        verbose_name_plural = 'images (unprocessed)'


class ProcessedImage(BaseMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_RAW_IMAGE),
        ]
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
    subdirectory_path = 'images/raw/'
    image_path = 'images/processed/'
    output_mode = 'RGB'
    content_type = 'image/png'
    file_format = 'PNG'
    file_extension = 'png'
    check_fields = [
        'saved_file',
        'processed_file',
    ]
    def image_url(self):
        if self.saved_file:
            return '{}' .format(self.processed_file.url)
        else:
            return 'No file'
    def image_link(self):
        if self.saved_file:
            return '<a href="{}" target="_blank">Image link</a>' .format(self.image_url())
        else:
            return 'No file'
    image_link.short_description = 'image link'
    image_link.allow_tags = True
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
    subdirectory_path = 'pdf/public/'
    class Meta:
        verbose_name = 'PDF (public)'
        verbose_name_plural = 'PDFs (public)'


class PrivatePDF(BaseMixin, PDFMixin, TitledMixin, PrivateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    subdirectory_path = 'pdf/private/'
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
    subdirectory_path = 'pdf/temporary/'
    class Meta:
        verbose_name = 'PDF (temporary)'
        verbose_name_plural = 'PDFs (temporary)'
