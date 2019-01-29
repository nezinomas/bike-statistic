from django import forms
from django.forms.models import modelformset_factory

from crispy_forms import layout
from crispy_forms.helper import FormHelper

from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput

from . import models
from ..core.helpers.form_helpers import set_field_properties


class DataForm(forms.ModelForm):
    class Meta:
        model = models.Data
        fields = '__all__'
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'checked': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)


class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=MonthPickerInput().start_of('event days'),
    )
    end_date = forms.DateField(
        widget=MonthPickerInput().end_of('event days'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.form_class = 'filter'
        self.helper.form_show_labels = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div('start_date', css_class='col'),
                layout.Div('end_date', css_class='col'),
                layout.Div(layout.Submit('date_filter', 'Filter'), css_class='col-1 btn_filter'),
                css_class='row')
        )
