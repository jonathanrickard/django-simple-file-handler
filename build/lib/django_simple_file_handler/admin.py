from django import (
    forms
)
from django.contrib import (
    admin
)


from .file_types import (
    CHECK_DOC,
    CHECK_WEB_IMAGE,
)
from .models import (
    PrivateDocument,
    PrivatePDF,
    ProcessedImage,
    PublicDocument,
    PublicPDF,
    TemporaryDocument,
    TemporaryPDF,
    UnprocessedImage,
)
from .validators import (
    CheckExtMIME,
)


class BaseAdmin(admin.ModelAdmin):
    actions = None
    search_fields = [
        'title',
        'extra_text',
    ]
    basic_readonly_fields = [
        'created',
        'updated',
    ]
    private_readonly_fields = [
        'title',
        'extra_text',
        'saved_file',
    ]
    readonly_fields = basic_readonly_fields + private_readonly_fields
    top_fieldsets = [
        (
            None, {
                'fields': [
                    'title',
                    'extra_text',
                    'saved_file',
                ],
            }
        ),
    ]
    bottom_fieldsets = [
        (
            'Date and time information', {
                'fields': [
                    'created',
                    'updated',
                ],
                'classes': [
                    'collapse',
                ],
            }
        ),
    ]
    fieldsets = top_fieldsets + bottom_fieldsets
    list_display = [
        'title',
        'file_link',
        'updated',
    ]
    ordering = [
        'title',
    ]
    list_per_page = 20


class ReadOnlyAdmin(BaseAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        more_context = {
            'remove_buttons': True,
        }
        more_context.update(extra_context or {})
        return super().change_view(request, object_id, form_url, more_context)


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


class PublicDocumentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_DOC))


class PublicDocumentAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = self.basic_readonly_fields
    form = PublicDocumentForm


admin.site.register(
    PublicDocument,
    PublicDocumentAdmin,
)


class PrivateDocumentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_DOC))


class PrivateDocumentAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = self.basic_readonly_fields
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


class TemporaryDocumentAdmin(ReadOnlyAdmin):
    pass


admin.site.register(
    TemporaryDocument,
    TemporaryDocumentAdmin,
)


class UnprocessedImageForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_WEB_IMAGE))


class UnprocessedImageAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = self.basic_readonly_fields
    form = UnprocessedImageForm


admin.site.register(
    UnprocessedImage,
    UnprocessedImageAdmin,
)


class ProcessedImageAdmin(ReadOnlyAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = [
            'output_width',
            'output_height',
            'processed_file',
            'extra_text',
            'saved_file',
        ] + self.basic_readonly_fields
        self.fieldsets = [
            (
                None, {
                    'fields': [
                        'processed_file',
                        'saved_file',
                        'output_width',
                        'output_height',
                        'extra_text',
                    ]
                }
            ),
        ] + self.bottom_fieldsets
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


class PublicPDFAdmin(ReadOnlyAdmin):
    pass


admin.site.register(
    PublicPDF,
    PublicPDFAdmin,
)


class PrivatePDFAdmin(ReadOnlyAdmin):
    list_display = [
        'title',
        'proxy_link',
        'updated',
    ]


admin.site.register(
    PrivatePDF,
    PrivatePDFAdmin,
)


class TemporaryPDFAdmin(ReadOnlyAdmin):
    pass


admin.site.register(
    TemporaryPDF,
    TemporaryPDFAdmin,
)
