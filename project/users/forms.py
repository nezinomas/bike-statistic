from crispy_forms.helper import FormHelper
from django.forms import ModelForm, PasswordInput

from ..core.lib import utils
from .models import User


class ExternalUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['garmin_user', 'garmin_password']
        widgets = {
            'garmin_password': PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user = utils.get_user()
        self.fields['garmin_user'].initial = self._user.garmin_user

        self.helper = FormHelper()

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        self._user.garmin_user = instance.garmin_user
        self._user.garmin_password = instance.garmin_password

        self._user.save()
