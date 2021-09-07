from django import forms
from django.core.validators import FileExtensionValidator


class UploadPriceFileForm(forms.Form):
    file = forms.FileField()


class ItemImageForm(forms.Form):
    image_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                  validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg'])],
                                  required=False)

