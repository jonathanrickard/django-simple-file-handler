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
    readonly_fields = [
        'created',
        'updated',
    ]
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


class BaseForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={
            'required': 'Please enter a title.',
            'unique': 'This title is already in use.',
        }
    )

    class Meta:
        fields = [
            'title',
            'extra_text',
            'saved_file',
        ]


class PublicDocumentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_DOC))

    BaseForm.Meta.model = PublicDocument


class PublicDocumentAdmin(BaseAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if obj and not self.has_change_permission(request, obj):
            return super().get_form(request, obj, **kwargs)
        return PublicDocumentForm


admin.site.register(
    PublicDocument,
    PublicDocumentAdmin,
)


class PrivateDocumentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_DOC))

    BaseForm.Meta.model = PrivateDocument


class PrivateDocumentAdmin(BaseAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if obj and not self.has_change_permission(request, obj):
            return super().get_form(request, obj, **kwargs)
        return PrivateDocumentForm

    list_display = [
        'title',
        'proxy_link',
        'updated',
    ]


admin.site.register(
    PrivateDocument,
    PrivateDocumentAdmin,
)


class TemporaryDocumentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_DOC))

    BaseForm.Meta.model = PublicDocument


class TemporaryDocumentAdmin(BaseAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if obj and not self.has_change_permission(request, obj):
            return super().get_form(request, obj, **kwargs)
        return TemporaryDocumentForm


admin.site.register(
    TemporaryDocument,
    TemporaryDocumentAdmin,
)


class UnprocessedImageForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saved_file'].validators.append(CheckExtMIME(allowed_attributes=CHECK_WEB_IMAGE))

    BaseForm.Meta.model = UnprocessedImage


class UnprocessedImageAdmin(BaseAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if obj and not self.has_change_permission(request, obj):
            return super().get_form(request, obj, **kwargs)

        return UnprocessedImageForm


admin.site.register(
    UnprocessedImage,
    UnprocessedImageAdmin,
)


class ProcessedImageAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = [
            'processed_file',
        ] + self.readonly_fields
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


class BasePDFAdmin(BaseAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readonly_fields = [
            'title',
            'extra_text',
            'saved_file',
        ] + self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return False


class PublicPDFAdmin(BasePDFAdmin):
    pass


admin.site.register(
    PublicPDF,
    PublicPDFAdmin,
)


class PrivatePDFAdmin(BasePDFAdmin):
    list_display = [
        'title',
        'proxy_link',
        'updated',
    ]


admin.site.register(
    PrivatePDF,
    PrivatePDFAdmin,
)


class TemporaryPDFAdmin(BasePDFAdmin):
    pass


admin.site.register(
    TemporaryPDF,
    TemporaryPDFAdmin,
)
