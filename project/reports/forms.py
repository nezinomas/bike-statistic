from django import forms
from django.forms.models import modelformset_factory

from crispy_forms import layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions

from bootstrap_datepicker_plus import DatePickerInput

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
                        css_class="form-control-sm"),
                ),
                layout.Column(
                    layout.Field(
                        'date',
                        css_class="form-control-sm"),
                ),
                layout.Column(
                    layout.Field(
                        'distance',
                        css_class="form-control-sm"),
                    css_class='short_int'
                ),
                layout.Column(
                    layout.Field(
                        'time',
                        style="width:auto;",
                        css_class="form-control-sm"),
                ),
                layout.Column(
                    layout.Field(
                        'temperature',
                        css_class="form-control-sm"),
                    css_class='short_int'
                ),
                layout.Column(
                    layout.Field(
                        'ascent',
                        css_class="form-control-sm"),
                    css_class='short_int'
                ),
                layout.Column(
                    layout.Field(
                        'descent',
                        css_class="form-control-sm"),
                    css_class='short_int'
                ),
            )
        )
        self.render_required_fields = True
        self.form_show_labels = False

        self.add_input(layout.Submit('submit', 'Save', css_class='button-sm'))

        # self.template = 'bootstrap4/table_inline_formset.html'
