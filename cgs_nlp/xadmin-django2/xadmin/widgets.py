"""
Form Widget classes specific to the Django admin site.
"""
from __future__ import absolute_import
from django import forms


class RadioChoiceInput(object):
    """Compatibility shim for Django versions without RadioChoiceInput."""

    def __init__(self, name, value, attrs, choice, index):
        self.name = name
        self.value = value
        self.attrs = attrs or {}
        self.choice_value, self.choice_label = choice
        self.index = index

    def _is_checked(self):
        if self.value is None:
            return False
        if isinstance(self.value, (list, tuple, set)):
            values = {force_str(v) for v in self.value}
            return force_str(self.choice_value) in values
        return force_str(self.value) == force_str(self.choice_value)

    def tag(self):
        attrs = dict(self.attrs)
        attrs.pop('inline', None)
        attrs_str = ''.join(
            ' %s="%s"' % (k, force_str(v))
            for k, v in attrs.items()
            if v is not None
        )
        checked = ' checked="checked"' if self._is_checked() else ''
        return mark_safe(
            '<input type="radio" name="%s" value="%s"%s%s />'
            % (force_str(self.name), force_str(self.choice_value), attrs_str, checked)
        )
from django.utils.encoding import force_str

from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.translation import gettext as _

from .util import vendor


class AdminDateWidget(forms.DateInput):

    @property
    def media(self):
        return vendor('datepicker.js', 'datepicker.css', 'xadmin.widget.datetime.js')

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'date-field form-control', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminDateWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super(AdminDateWidget, self).render(name, value, attrs, renderer)
        return mark_safe('<div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><i class="fa fa-calendar"></i></span>%s'
                         '<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (input_html, _(u'Today')))


class AdminTimeWidget(forms.TimeInput):

    @property
    def media(self):
        return vendor('datepicker.js', 'clockpicker.js', 'clockpicker.css', 'xadmin.widget.datetime.js')

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'time-field form-control', 'size': '8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTimeWidget, self).__init__(attrs=final_attrs, format=format)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super(AdminTimeWidget, self).render(name, value, attrs, renderer)
        return mark_safe('<div class="input-group time bootstrap-clockpicker"><span class="input-group-addon"><i class="fa fa-clock-o">'
                         '</i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>' % (input_html, _(u'Now')))


class AdminSelectWidget(forms.Select):

    @property
    def media(self):
        return vendor('select.js', 'select.css', 'xadmin.widget.select.js')


class AdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        rendered = str(super(AdminSplitDateTime, self).render(name, value, attrs, renderer))
        input_html = [ht for ht in rendered.replace('><input', '>\n<input').split('\n') if ht != '']
        # return input_html
        return mark_safe('<div class="datetime clearfix"><div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><i class="fa fa-calendar"></i></span>%s'
                         '<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>'
                         '<div class="input-group time bootstrap-clockpicker"><span class="input-group-addon"><i class="fa fa-clock-o">'
                         '</i></span>%s<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div></div>' % (input_html[0], _(u'Today'), input_html[1], _(u'Now')))

    def format_output(self, rendered_widgets):
        return mark_safe(u'<div class="datetime clearfix">%s%s</div>' %
                         (rendered_widgets[0], rendered_widgets[1]))


class AdminRadioSelect(forms.RadioSelect):
    pass


class AdminCheckboxSelect(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        attrs = attrs or {}
        has_id = 'id' in attrs
        final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})
        output = []
        # Normalize to strings
        str_values = set([force_str(v) for v in value])
        choices = self.choices if isinstance(self.choices, (list, tuple)) else []
        for i, (option_value, option_label) in enumerate(choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs.get('id'), i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(
                final_attrs, check_test=lambda value: value in str_values)
            option_value = force_str(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_str(option_label))

            if final_attrs.get('inline', False):
                output.append(u'<label%s class="checkbox-inline">%s %s</label>' % (label_for, rendered_cb, option_label))
            else:
                output.append(u'<div class="checkbox"><label%s>%s %s</label></div>' % (label_for, rendered_cb, option_label))
        return mark_safe(u'\n'.join(output))


class AdminSelectMultiple(forms.SelectMultiple):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'select-multi'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSelectMultiple, self).__init__(attrs=final_attrs)


class AdminFileWidget(forms.ClearableFileInput):
    template_with_initial = (u'<p class="file-upload">%s</p>'
                             % forms.ClearableFileInput.initial_text)
    template_with_clear = (u'<span class="clearable-file-input">%s</span>'
                           % forms.ClearableFileInput.clear_checkbox_label)


class AdminTextareaWidget(forms.Textarea):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'textarea-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextareaWidget, self).__init__(attrs=final_attrs)


class AdminTextInputWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'text-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextInputWidget, self).__init__(attrs=final_attrs)


class AdminURLFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'url-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminURLFieldWidget, self).__init__(attrs=final_attrs)


class AdminIntegerFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'int-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminIntegerFieldWidget, self).__init__(attrs=final_attrs)


class AdminCommaSeparatedIntegerFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'sep-int-field'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminCommaSeparatedIntegerFieldWidget,
              self).__init__(attrs=final_attrs)
