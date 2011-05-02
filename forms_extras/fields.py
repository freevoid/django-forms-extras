from django import forms
from django.utils.translation import ugettext_lazy as _

from forms_extras.declarative import DeclarativeMultiWidget,\
    DeclarativeMultiValueField

from forms_extras.widgets import DatePeriodSelectInput, Period


class NoneBooleanField(forms.BooleanField):
    def to_python(self, value):
        original = super(NoneBooleanField, self).to_python(value)
        return original if original else None


class DatePeriodSelectField(forms.MultiValueField):
    '''
    Form field for a date period with predefined choices
    (today, month ago, etc).
    '''
    widget = DatePeriodSelectInput

    def __init__(self, *args, **kwargs):
        super(DatePeriodSelectField, self).__init__(
                (forms.ChoiceField(
                    choices=Period.CHOICES + [('select', _('Select period...'))]),
                    forms.DateField(), forms.DateField()),
                *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            type = data_list[0]
            if type == 'select':
                return data_list[1], data_list[2]
            else:
                return Period.get_span(type)
        else:
            return None


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
