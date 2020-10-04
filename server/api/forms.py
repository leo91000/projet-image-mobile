from django import forms


class ImageFileForm(forms.Form):
    image_file = forms.ImageField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
