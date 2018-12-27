from django import forms
from django.forms.models import modelformset_factory

from crispy_forms import layout
from crispy_forms.helper import FormHelper

from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput

from . import models


class DataForm(forms.ModelForm):
    class Meta:
        model = models.Data
        fields = ['bike', 'date', 'time', 'distance', 'temperature', 'ascent', 'descent']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
        }


DataFormset = modelformset_factory(models.Data, exclude=(), extra=1, form=DataForm)


class DataFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form_method = 'post'
        self.layout = layout.Layout(
            layout.Row(
                layout.Column(
                    layout.Field(
                        'bike',
                        css_class='form-control-sm'),
                    css_class = 'col-lg-2'
                ),
                layout.Column(
                    layout.Field(
                        'date',
                        css_class='form-control-sm'),
                    css_class='col-lg-3'
                ),
                layout.Column(
                    layout.Field(
                        'distance',
                        css_class='form-control-sm'),
                     css_class='col-lg-2'
                ),
                layout.Column(
                    layout.Field(
                        'time',
                        css_class='form-control-sm'),
                    css_class='col-lg-2'
                ),
                layout.Column(
                    layout.Field(
                        'temperature',
                        css_class='form-control-sm'),
                    css_class='col-lg-1'
                ),
                layout.Column(
                    layout.Field(
                        'ascent',
                        css_class='form-control-sm'),
                    css_class='col-lg-1'
                ),
                layout.Column(
                    layout.Field(
                        'descent',
                        css_class='form-control-sm'),
                    css_class='col-lg-1'
                ),
            )
        )
        self.render_required_fields = True
        self.form_show_labels = False

        self.form_class = 'data'
        self.add_input(layout.Submit('submit', 'Save', css_class='button-sm'))

        # self.template = 'bootstrap4/table_inline_formset.html'


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
