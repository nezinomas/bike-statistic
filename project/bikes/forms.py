from datetime import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from django import forms

from ..core.mixins.form_mixin import FormMixin
from .models import Bike, BikeInfo, Component, ComponentWear


class ComponentForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()


class ComponentWearForm(forms.ModelForm):
    class Meta:
        model = ComponentWear
        fields = ['start_date', 'end_date', 'price', 'brand']

        widgets = {
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        self._bike_slug = kwargs.pop('bike_slug', None)
        self._component_pk = kwargs.pop('component_pk', None)

        super().__init__(*args, **kwargs)

        self.fields['start_date'].initial = datetime.now()
        self.helper = FormHelper()

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        if self._bike_slug:
            instance.bike = Bike.objects.related().get(slug=self._bike_slug)
        if self._component_pk:
            instance.component = Component.objects.related().get(pk=self._component_pk)

        instance.save()

        return instance

    def clean(self):
        cleaned = super().clean()

        started = cleaned.get("start_date")
        ended = cleaned.get("end_date")

        if ended and started and ended < started:
            self.add_error(
                "end_date", "End date cannot be earlier than start date."
            )

        #  check if all component are closed
        if not self.instance.pk and ComponentWear.objects.items().filter(end_date__isnull=True).count() > 0:
            raise forms.ValidationError(
                "All components must be closed."
            )

        return cleaned


class BikeForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Bike
        fields = [
            'date',
            'full_name',
            'short_name',
            'main',
            'retired',
        ]
        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = datetime.now()

        self.helper = FormHelper()

    def clean_main(self):
        _main = self.cleaned_data.get('main')

        qs = Bike.objects.items().filter(main=True)

        # exclude self if update
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if _main and qs.count() > 0:
            raise forms.ValidationError('There can be only one main bike.')

        return _main

    def clean_retired(self):
        _main = self.cleaned_data.get('main')
        _retired = self.cleaned_data.get('retired')

        if _main and _retired:
            raise forms.ValidationError('The main bike cannot be marked as Retired!')

        return _retired


class BikeInfoForm(forms.ModelForm):
    class Meta:
        model = BikeInfo
        fields = ['component', 'description']

    def __init__(self, *args, **kwargs):
        self._bike_slug = kwargs.pop('bike_slug', None)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        if self._bike_slug:
            instance.bike = Bike.objects.related().get(slug=self._bike_slug)

        instance.save()

        return instance
