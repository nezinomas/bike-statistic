from crispy_forms.helper import FormHelper
from django.forms import ModelForm, PasswordInput

from ..core.helpers.form_helpers import set_field_properties
from ..core.lib import utils
from .models import User


class ExternalUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['endomondo_user', 'endomondo_password']
        widgets = {
            'endomondo_password': PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user = utils.get_user()
        self.fields['endomondo_user'].initial = self._user.endomondo_user

        self.helper = FormHelper()
        set_field_properties(self, self.helper)

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)

        self._user.endomondo_user = instance.endomondo_user
        self._user.endomondo_password = instance.endomondo_password

        self._user.save()
