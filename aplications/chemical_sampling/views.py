from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SamplingForm, TemplatesFormSet
from .models import ModelChemicalSampling, ModelTemplates
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from tools.odoo_query import TemplateManager


@login_required
def feed_view(request):
     if request.user.is_authenticated:
          print(f"Usuario autenticado: {request.user.username}")
     else:
          print("Usuario no autenticado.")

     return render(request, 'sampling/feed.html', {'ping': 'pong'})


@login_required
def create_sampling_view(request):
    if request.method == 'POST':
        sampling_form = SamplingForm(request.POST)
        formset = TemplatesFormSet(request.POST)

        if sampling_form.is_valid() and formset.is_valid():
            sampling = sampling_form.save(commit=False)
            sampling.user = request.user
            sampling.save()

            for form in formset:
                template = form.save(commit=False)
                template.id_chemical_samples = sampling
                template.save()

            messages.success(request, "Los datos se han guardado correctamente.")
            return redirect('sampling:feed')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        sampling_form = SamplingForm()
        formset = TemplatesFormSet(queryset=ModelTemplates.objects.none())

    return render(request, 'sampling/create.html', {
        'sampling_form': sampling_form,
        'formset': formset,
        'user': request.user,
        'profile': request.user.profile
    })

""" ------------------------
     .: AJAX VIEWS :.
--------------------------- """


class TemplateSuggestionsView(TemplateView):
    def get(self, request,*args,**kwargs):
        template_name = request.GET.get('template_name', '')
        template_manager = TemplateManager()
        suggestions = template_manager.fetch_template_suggestions(template_name)
        return JsonResponse(suggestions, safe=False)


class TemplateDetailsView(TemplateView):
    def get(self, request,*args,**kwargs):
        template_name = request.GET.get('template_name', '')
        template_manager = TemplateManager()
        template_data = template_manager.fetch_exact_template_data(template_name)
        return JsonResponse(template_data, safe=False)







