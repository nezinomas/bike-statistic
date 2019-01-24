from crispy_forms.helper import FormHelper

from django import forms

from .models import Component, ComponentStatistic
from ..core.helpers.form_helpers import set_field_properties


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)


class ComponentStatisticForm(forms.ModelForm):
    class Meta:
        model = ComponentStatistic
        fields = '__all__'
        widgets = {
            'bike': forms.HiddenInput(),
            'component': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
