from django import (
    forms
)
from django.contrib import (
    admin
)


from .models import *


class BaseForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={
            'required': 'Please enter a title.',
            'unique': 'This title is already in use.',
        }
    )


class BaseAdmin(admin.ModelAdmin):
    actions = None
    search_fields = [
        'title',
        'extra_text',
    ]
    readonly_fields = [
        'created',
        'updated',
    ]
    fieldsets = [
        (
            None, {
                'fields': [
                    'title',
                    'extra_text',
                    'saved_file',
                ]
            }
        ),
        (
            'Date and time information', {
                'fields': [
                    'created',
                    'updated',
                ],
                'classes': [
                    'collapse',
                ]
            }
        ),
    ]
    list_display = [
        'title',
        'file_link',
        'updated',
    ]
    ordering = ('title',)
    list_per_page = 20


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, form_url='', extra_context=None):
        more_context = {
            'remove_buttons': True,
        }
        more_context.update(extra_context or {})
        return super().change_view(request, object_id, form_url, more_context)


class PublicDocumentForm(BaseForm):
    class Meta:
        model = PublicDocument
        fields = [
            'extra_text',
            'saved_file',
        ]


class PublicDocumentAdmin(BaseAdmin):
    form = PublicDocumentForm


admin.site.register(
    PublicDocument,
    PublicDocumentAdmin,
)


class PrivateDocumentForm(BaseForm):
    class Meta:
        model = PrivateDocument
        fields = [
            'extra_text',
            'saved_file',
        ]


class PrivateDocumentAdmin(BaseAdmin):
    form = PrivateDocumentForm
    list_display = [
        'title',
        'proxy_link',
        'updated',
    ]


admin.site.register(
    PrivateDocument,
    PrivateDocumentAdmin,
)


class TemporaryDocumentAdmin(BaseAdmin, ReadOnlyAdmin):
    readonly_fields = [
        'created',
        'updated',
        'title',
        'extra_text',
        'saved_file',
    ]


admin.site.register(
    TemporaryDocument,
    TemporaryDocumentAdmin,
)


class UnprocessedImageForm(BaseForm):
    class Meta:
        model = UnprocessedImage
        fields = [
            'extra_text',
            'saved_file',
        ]


class UnprocessedImageAdmin(BaseAdmin):
    form = UnprocessedImageForm


admin.site.register(
    UnprocessedImage,
    UnprocessedImageAdmin,
)


class ProcessedImageAdmin(BaseAdmin, ReadOnlyAdmin):
    search_fields = [
        'generated_name',
    ]
    readonly_fields = [
        'created',
        'updated',
        'generated_name',
        'output_width',
        'output_height',
        'processed_file',
        'saved_file',
    ]
    fieldsets = [
        (
            None, {
                'fields': [
                    'generated_name',
                    'output_width',
                    'output_height',
                    'processed_file',
                    'saved_file',
                ]
            }
        ),
        (
            'Date and time information', {
                'fields': [
                    'created',
                    'updated',
                ],
                'classes': [
                    'collapse',
                ]
            }
        ),
    ]
    list_display = [
        'generated_name',
        'image_link',
        'updated',
    ]
    ordering = ('generated_name',)


admin.site.register(
    ProcessedImage,
    ProcessedImageAdmin,
)


class PublicPDFAdmin(BaseAdmin, ReadOnlyAdmin):
    readonly_fields = [
        'created',
        'updated',
        'title',
        'extra_text',
        'saved_file',
    ]


admin.site.register(
    PublicPDF,
    PublicPDFAdmin,
)


class PrivatePDFAdmin(BaseAdmin, ReadOnlyAdmin):
    readonly_fields = [
        'created',
        'updated',
        'title',
        'extra_text',
        'saved_file',
    ]
    list_display = [
        'title',
        'proxy_link',
        'updated',
    ]


admin.site.register(
    PrivatePDF,
    PrivatePDFAdmin,
)


class TemporaryPDFAdmin(BaseAdmin, ReadOnlyAdmin):
    readonly_fields = [
        'created',
        'updated',
        'title',
        'extra_text',
        'saved_file',
    ]


admin.site.register(
    TemporaryPDF,
    TemporaryPDFAdmin,
)
