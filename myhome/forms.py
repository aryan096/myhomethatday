import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class SearchDateForm(forms.Form):
    search_date = forms.DateField(required=True, label="Date")

    # validation date fucntion
    def clean_search_date(self):
        data = self.cleaned_data['search_date']

        # Check if a date is not in the future
        if data > datetime.date.today():
            raise ValidationError(_('Please enter a day that has happened'))

        # # Check if a date is in the allowed range .
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data
