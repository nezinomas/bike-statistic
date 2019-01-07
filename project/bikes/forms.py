from crispy_forms import layout
from crispy_forms.helper import FormHelper

from django import forms

from .models import Component


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control-sm'

        self.helper = FormHelper()
        self.helper.form_show_labels = False
