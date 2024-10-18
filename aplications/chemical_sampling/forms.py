from django import forms
from django.forms import modelformset_factory
from .models import ModelChemicalSampling, ModelTemplates

# Formulario principal para el modelo ModelChemicalSampling
class SamplingForm(forms.ModelForm):
    class Meta:
        model = ModelChemicalSampling
        fields = ['user', 'profile', 'type_test', 'analyst_request', 'priority', 'id_template', 'templates', 'product_db', 'description', 'method', 'state']

# Formulario para ModelTemplates
class TemplatesForm(forms.ModelForm):
    class Meta:
        model = ModelTemplates
        fields = ['t_number', 'test_name', 'test_time', 'astmd', 'min_val', 'recurrent_val', 'max_val', 'val_result', 'price_unit']

# Formset para manejar múltiples plantillas relacionadas con ModelChemicalSampling
TemplatesFormSet = modelformset_factory(ModelTemplates, form=TemplatesForm, extra=1)
