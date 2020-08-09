import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

my_default_errors = {
    'required': 'Please enter a valid date (yyyy-mm-dd)',
    'invalid': 'Please enter a valid date (yyyy-mm-dd)'
}

class SearchDateForm(forms.Form):
    search_date = forms.DateField(required=True, label="", error_messages=my_default_errors)

    # validation date fucntion
    def clean_search_date(self):
        data = self.cleaned_data['search_date']

        # Check if a date is not in the future
        if data > datetime.date.today():
            raise ValidationError(_('Please enter a date in the past!'))

        return data
