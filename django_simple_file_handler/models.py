from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.db import (
    models,
)
from django.db.models.signals import (
    pre_delete,
    pre_save,
)
from django.dispatch.dispatcher import (
    receiver,
)
from django.urls import (
    reverse,
)


from .dictionaries import *
from .functions import *
from .storage import *
from .validators import *


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
        storage=RemoveOldFile(),
        upload_to=create_file_path,
        validators=[],
        max_length=254,
    )
    def file_url(self):
        if self.saved_file:
            return '{0}' .format(self.saved_file.url)
        else:
            return 'No file'
    file_url.short_description = 'file URL'
    def file_link(self):
        if self.saved_file:
            return '<a href="{0}" target="_blank">File link</a>' .format(self.file_url())
        else:
            return 'No file'
    file_link.short_description = 'file link'
    file_link.allow_tags = True
    class Meta:
        abstract = True


class TitledMixin(models.Model):
    title = models.CharField(
        max_length=254,
        blank=False,
        unique=True,
    )
    def __str__(self):
        return self.title
    class Meta:
        abstract = True


class PublicMixin(models.Model):
    def save(self, *args, **kwargs):
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
            return '<a href="{0}" target="_blank">Proxy link</a>' .format(self.proxy_url())
        else:
            return 'No file'
    proxy_link.short_description = 'proxy link'
    proxy_link.allow_tags = True
    def save(self, *args, **kwargs):
        if self.saved_file:
            self.proxy_slug = create_proxy(self)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


class TemporaryMixin(models.Model):
    def save(self, *args, **kwargs):
        self.generated_name = create_slug_with_key(self.title)
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


class PDFMixin(BaseMixin):
    def __init__(self, *args, **kwargs):
        self.template_location = kwargs.pop('template_location','')
        self.data = kwargs.pop('data',{})
        super().__init__(*args, **kwargs)
    def save(self, *args, **kwargs):
        self.saved_file = create_pdf(
            self.generated_name,
            self.template_location,
            self.data,
        )
        super().save(*args, **kwargs)
    class Meta:
        abstract = True


class PublicDocument(BaseMixin, TitledMixin, PublicMixin):
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
    def save(self, *args, **kwargs):
        self.generated_name = create_key(128)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'document (private)'
        verbose_name_plural = 'documents (private)'


class TemporaryDocument(BaseMixin, TitledMixin, TemporaryMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('saved_file').validators = [
            CheckExtMIME(allowed_attributes=CHECK_DOC),
        ]
    subdirectory_path = 'documents/temporary/'
    class Meta:
        verbose_name = 'document (temporary)'
        verbose_name_plural = 'documents (temporary)'


class UnprocessedImage(BaseMixin, TitledMixin, PublicMixin):
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
        storage=RemoveOldFile(),
        upload_to='images/processed/',
        blank=True,
        null=True,
    )
    subdirectory_path = 'images/raw/'
    output_mode = 'RGB'
    content_type = 'image/png'
    file_format = 'PNG'
    file_extension = 'png'
    def image_url(self):
        if self.saved_file:
            return '{0}' .format(self.processed_file.url)
        else:
            return 'No file'
    def image_link(self):
        if self.saved_file:
            return '<a href="{0}" target="_blank">Image link</a>' .format(self.image_url())
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
        try:
            saved_object = ProcessedImage.objects.get(pk=self.pk)
            changeable_fields = [
                'saved_file',
                'output_width',
                'output_height',
            ]
            for field in changeable_fields:
                if getattr(self, field) != getattr(saved_object, field):
                    self.processed_file=process_image(*image_args)
                    break
        except ObjectDoesNotExist:
            self.generated_name = create_key(length=32)
            self.processed_file=process_image(*image_args)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'image (processed)'
        verbose_name_plural = 'images (processed)'


class PublicPDF(PublicMixin, PDFMixin, TitledMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    subdirectory_path = 'pdf/public/'
    class Meta:
        verbose_name = 'PDF (public)'
        verbose_name_plural = 'PDFs (public)'


class PrivatePDF(PDFMixin, TitledMixin, PrivateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    subdirectory_path = 'pdf/private/'
    proxy_reverse = 'django_simple_file_handler:proxy_pdf'
    def save(self, *args, **kwargs):
        self.generated_name = create_key(length=128)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'PDF (private)'
        verbose_name_plural = 'PDFs (private)'


class TemporaryPDF(TemporaryMixin, PDFMixin, TitledMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    subdirectory_path = 'pdf/temporary/'
    class Meta:
        verbose_name = 'PDF (temporary)'
        verbose_name_plural = 'PDFs (temporary)'


@receiver(
    pre_save,
    sender=PublicDocument,
)
@receiver(
    pre_save,
    sender=PrivateDocument,
)
@receiver(
    pre_save,
    sender=TemporaryDocument,
)
@receiver(
    pre_save,
    sender=UnprocessedImage,
)
@receiver(
    pre_save,
    sender=PublicPDF,
)
@receiver(
    pre_save,
    sender=PrivatePDF,
)
@receiver(
    pre_save,
    sender=TemporaryPDF,
)
def saved_file_compare(sender, instance, **kwargs):
    file_compare(
        instance,
        fields=[
            'saved_file',
        ],
        **kwargs,
    )


@receiver(
    pre_save,
    sender=ProcessedImage,
)
def processed_file_compare(sender, instance, **kwargs):
    file_compare(
        instance,
        fields=[
            'saved_file',
            'processed_file',
        ],
        **kwargs,
    )


@receiver(
    pre_delete,
    sender=PublicDocument,
)
@receiver(
    pre_delete,
    sender=PrivateDocument,
)
@receiver(
    pre_delete,
    sender=TemporaryDocument,
)
@receiver(
    pre_delete,
    sender=UnprocessedImage,
)
@receiver(
    pre_delete,
    sender=PublicPDF,
)
@receiver(
    pre_delete,
    sender=PrivatePDF,
)
@receiver(
    pre_delete,
    sender=TemporaryPDF,
)
def saved_file_delete(sender, instance, **kwargs):
    file_delete(
        instance,
        fields=[
            'saved_file',
        ],
        **kwargs,
    )


@receiver(
    pre_delete,
    sender=ProcessedImage,
)
def processed_file_delete(sender, instance, **kwargs):
    file_delete(
        instance,
        fields=[
            'saved_file',
            'processed_file',
        ],
        **kwargs,
    )
