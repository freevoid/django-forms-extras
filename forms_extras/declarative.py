import itertools

from django import forms
from django.utils.datastructures import SortedDict


def expand_initials(initial_dict):
    for k, v in initial_dict.iteritems():
        if callable(v):
            initial_dict[k] = v()
    return initial_dict


class DeclarativeMultiWidget(forms.MultiWidget):
    def __init__(self, widgets_template, required=False, *args, **kwargs):
        self.required = required
        self.widgets_order = []
        widgets = []
        for name, klass, widget_kwargs in widgets_template:
            self.widgets_order.append(name)
            widgets.append(klass(**widget_kwargs))
        super(DeclarativeMultiWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        super_ = super(DeclarativeMultiWidget, self).format_output(rendered_widgets)

        if self.required:
            return u'<div class="required">%s</div>' % super_
        else:
            return super_

    def decompress(self, value):
        if value is None:
            return ''
        elif isinstance(value, dict):
            return [value.get(key) for key in self.widgets_order]
        elif isinstance(value, basestring):
            return [value]
        else:
            raise NotImplementedError


class DeclarativeMultiValueFieldMeta(type):
    def __new__(cls, name, bases, attrs):
        wt = attrs.get('widgets_template')
        ft = attrs.get('fields_template')
        if wt and ft:
            subwidget_names = zip(*wt)[0]
            name_to_field_mapping = SortedDict(zip(subwidget_names, ft))
            attrs['field_mapping'] = name_to_field_mapping
            attrs['field_names'] = subwidget_names
        return super(DeclarativeMultiValueFieldMeta, cls).__new__(cls, name, bases, attrs)


class DeclarativeMultiValueField(forms.MultiValueField):
    __metaclass__ = DeclarativeMultiValueFieldMeta
    required = False
    widget_class = DeclarativeMultiWidget

    def __init__(self, *args, **kwargs):

        self.widget = self.widget_class(self.widgets_template, required=self.required)
        kwargs['label'] = kwargs.get('label') or getattr(self, 'label', None)
        initial = expand_initials(kwargs.pop('initial', {}))

        def field_generator():
            for name, (klass, field_kwargs) in self.field_mapping.iteritems():
                if not field_kwargs.has_key('initial') and initial.has_key(name):
                    field_kwargs['initial'] = initial[name]
                yield klass(**field_kwargs)

        fields = list(field_generator())

        super(DeclarativeMultiValueField, self).__init__(fields, *args, **kwargs)

    def clean(self, value):
        return super(DeclarativeMultiValueField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            return dict((field_name, data_list[i])\
                    for i, field_name in enumerate(
                        itertools.izip(*self.widgets_template).next()
                        ))
        else:
            return None

    @staticmethod
    def display(compressed):
        return compressed.values()[0] if len(compressed) else ''
