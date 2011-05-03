import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from forms_extras.declarative import DeclarativeMultiWidget,\
    DeclarativeMultiValueField


class CommaSeparatedCharField(forms.CharField):

    SEPARATORS_RE = re.compile(r'[,;\s]+')

    def clean(self, value):

        value = super(CommaSeparatedCharField, self).clean(value)

        if value:
            return filter(None, self.SEPARATORS_RE.split(value))
        else:
            return []


class NoneBooleanField(forms.BooleanField):

    def to_python(self, value):
        original = super(NoneBooleanField, self).to_python(value)
        return original if original else None


class DatePeriodWidget(DeclarativeMultiWidget):
    def format_output(self, widget_list):
        return _('from %(from_date)s to %(to_date)s') % {'from_date': widget_list[0],
            'to_date': widget_list[1]}


class DatePeriodField(DeclarativeMultiValueField):
    widget_class = DatePeriodWidget
    widgets_template = (
            ('from', forms.DateInput, {'attrs': {'style':'width:11ex;'}}),
            ('to', forms.DateInput, {'attrs': {'style':'width:11ex;'}})
        )

    fields_template = (
        (forms.DateField, {}),
        (forms.DateField, {})
        )
