from django import forms
from .models import GeoMeasureMent

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = GeoMeasureMent
        fields = ('destination',)