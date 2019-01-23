from crispy_forms.helper import FormHelper

from django import forms

from .models import Component, ComponentStatistic


def set_field_properties(self, helper):
    for field_name in self.fields:
        self.fields[field_name].widget.attrs['class'] = 'form-control-sm'

    helper.form_show_labels = False


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
