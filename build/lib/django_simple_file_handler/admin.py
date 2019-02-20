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
    class Meta:
        fields = [
            'extra_text',
            'saved_file',
        ]


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
    ordering = [
        'title',
    ]
    list_per_page = 20


class AdditionalFieldsAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fieldsets = [
            (
                None, {
                    'fields': [
                        'title',
                        'extra_text',
                        'saved_file',
                    ]
                }
            ),
        ] + self.fieldsets


class ReadOnlyFieldsAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = [
            'title',
            'extra_text',
            'saved_file',
        ] + self.readonly_fields


class ReadOnlyMethodsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, form_url='', extra_context=None):
        more_context = {
            'remove_buttons': True,
        }
        more_context.update(extra_context or {})
        return super().change_view(request, object_id, form_url, more_context)


class PrivateAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = [
            'title',
            'proxy_link',
            'updated',
        ]


class PublicDocumentForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = PublicDocument


class PublicDocumentAdmin(BaseAdmin, AdditionalFieldsAdmin):
    form = PublicDocumentForm


admin.site.register(
    PublicDocument,
    PublicDocumentAdmin,
)


class PrivateDocumentForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = PrivateDocument


class PrivateDocumentAdmin(PrivateAdmin, AdditionalFieldsAdmin):
    form = PrivateDocumentForm


admin.site.register(
    PrivateDocument,
    PrivateDocumentAdmin,
)


class TemporaryDocumentAdmin(BaseAdmin, AdditionalFieldsAdmin, ReadOnlyFieldsAdmin, ReadOnlyMethodsAdmin):
    pass


admin.site.register(
    TemporaryDocument,
    TemporaryDocumentAdmin,
)


class UnprocessedImageForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = UnprocessedImage


class UnprocessedImageAdmin(BaseAdmin, AdditionalFieldsAdmin):
    form = UnprocessedImageForm


admin.site.register(
    UnprocessedImage,
    UnprocessedImageAdmin,
)


class ProcessedImageAdmin(BaseAdmin, ReadOnlyMethodsAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = [
            'generated_name',
            'output_width',
            'output_height',
            'extra_text',
            'processed_file',
            'saved_file',
        ] + self.readonly_fields
        self.fieldsets = [
            (
                None, {
                    'fields': [
                        'generated_name',
                        'output_width',
                        'output_height',
                        'extra_text',
                        'processed_file',
                        'saved_file',
                    ]
                }
            ),
        ] + self.fieldsets
    search_fields = [
        'generated_name',
        'extra_text',
    ]
    list_display = [
        'generated_name',
        'image_link',
        'updated',
    ]
    ordering = [
        'generated_name',
    ]


admin.site.register(
    ProcessedImage,
    ProcessedImageAdmin,
)


class PublicPDFAdmin(BaseAdmin, AdditionalFieldsAdmin, ReadOnlyFieldsAdmin, ReadOnlyMethodsAdmin):
    pass


admin.site.register(
    PublicPDF,
    PublicPDFAdmin,
)


class PrivatePDFAdmin(PrivateAdmin, AdditionalFieldsAdmin, ReadOnlyFieldsAdmin, ReadOnlyMethodsAdmin):
    pass


admin.site.register(
    PrivatePDF,
    PrivatePDFAdmin,
)


class TemporaryPDFAdmin(BaseAdmin, AdditionalFieldsAdmin, ReadOnlyFieldsAdmin, ReadOnlyMethodsAdmin):
    pass


admin.site.register(
    TemporaryPDF,
    TemporaryPDFAdmin,
)
