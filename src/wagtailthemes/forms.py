from django import forms
from django.utils.translation import gettext as _

from wagtailthemes.models import Theme


class ImportForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        empty_label=_("Choose a theme"),
    )
    zip_file = forms.FileField()


class ExportForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        empty_label=_("Choose a theme"),
    )
