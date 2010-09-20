from django import forms
from models import Image
from widgets import AdminImageWidget

class ImageAdminForm(forms.ModelForm):
    
    snipshot_file = forms.CharField(required=False)
    
    class Meta:
        model = Image

    class Media:
        js = ("my_code.js",)

    def __init__(self, *args, **kwargs):
        super(ImageAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = AdminImageWidget()
        self.fields['image'].required = False

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self.instance.id:
            snipshot_file = cleaned_data.get('snipshot_file')
            image = cleaned_data.get('image')
            if not (snipshot_file or image):
                self._errors["image"] = self.error_class(['This field is required.'])
                del cleaned_data["image"]
        return cleaned_data