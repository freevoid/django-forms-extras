import datetime
from calendar import monthrange

from django import forms
from django.utils.translation import ugettext_lazy as _

class Period:
    """Time periods used in filtering forms"""
    
    CHOICES = [
        ('today', _('Today')),
        ('yesterday', _('Yesterday')),
        ('thisweek', _('This week')),
        ('lastweek', _('Last week')),
        ('thismonth', _('This month')),
        ('lastmonth', _('Last month')),
    ]
    
    class InvalidCode(Exception): pass
    
    @classmethod
    def get_span(cls, choice_code):
        """Get earliest and latest time boundaries corresponding to supplied code"""
        today = datetime.date.today()
        first_second = datetime.time(0,0,0)
        last_second = datetime.time(23,59,59)
        if choice_code == 'today':
            return (
                datetime.datetime.combine(today, first_second),
                datetime.datetime.combine(today, last_second),
            )
        elif choice_code == 'yesterday':
            yesterday = today - datetime.timedelta(days=1)
            return (
                datetime.datetime.combine(yesterday, first_second),
                datetime.datetime.combine(yesterday, last_second),
            )
        elif choice_code == 'thisweek':
            monday = today - datetime.timedelta(days=today.weekday())
            sunday = monday + datetime.timedelta(days=6)
            return (
                datetime.datetime.combine(monday, first_second),
                datetime.datetime.combine(sunday, last_second),
            )
        elif choice_code == 'lastweek':
            last_monday = today - datetime.timedelta(days=today.weekday()+7)
            last_sunday = last_monday + datetime.timedelta(days=6)
            return (
                datetime.datetime.combine(last_monday, first_second),
                datetime.datetime.combine(last_sunday, last_second),
            )
        elif choice_code == 'thismonth':
            (_, num_days) = monthrange(today.year, today.month)
            first_day_of_month = today.replace(day=1)
            last_day_of_month = today.replace(day=num_days)
            return (
                datetime.datetime.combine(first_day_of_month, first_second),
                datetime.datetime.combine(last_day_of_month, last_second),
            )
        elif choice_code == 'lastmonth':
            last_day_of_LAST_month = today.replace(day=1) - datetime.timedelta(days=1)
            first_day_of_LAST_month = last_day_of_LAST_month.replace(day=1)
            return (
                datetime.datetime.combine(first_day_of_LAST_month, first_second),
                datetime.datetime.combine(last_day_of_LAST_month, last_second),
            )
        raise cls.InvalidCode('can\'t generate time span: invalid choice_code = %s' % choice_code)

class DatePeriodSelectInput(forms.MultiWidget):
    '''
    Widget for DatePeriodSelectField
    '''
    widgets = [forms.Select(
        choices=Period.CHOICES + [('select', _('Select period...'))]),
        forms.DateInput(), forms.DateInput()]

    def __init__(self, attrs=None):
        super(DatePeriodSelectInput, self).__init__(self.widgets, attrs=attrs)

    def onready_js(self, name):
        return 'period_field("%(name)s_0", "%(name)s_1", "%(name)s_2");' % {'name': name}

    class Media:
        js = ('js/period_field.js',)

    def decompress(self, value):
        '''
        @param value: tuple of datetime instances
        @return: list of strings to represent widgets
        '''
        if value:
            from_, to = value
            return ['select', from_, to]
        else:
            return ['today', None, None]

    def format_output(self, widget_list):
        return u'%s<div class="detailed_period"><br />%s %s<br />%s %s</div>' % (
                widget_list[0], _('from'), widget_list[1], _('to'), widget_list[2])


