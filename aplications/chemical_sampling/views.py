from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SamplingForm, TemplatesFormSet
from .models import ModelChemicalSampling, ModelTemplates
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
        # Cargar los formularios con los datos enviados
        sampling_form = SamplingForm(request.POST)
        formset = TemplatesFormSet(request.POST)

        if sampling_form.is_valid() and formset.is_valid():
            # Guardar la instancia principal del modelo ModelChemicalSampling
            sampling = sampling_form.save(commit=False)
            sampling.user = request.user  # Asignamos el usuario actual
            sampling.save()

            # Guardar las instancias del formset, asociándolas con la instancia principal
            for form in formset:
                template = form.save(commit=False)
                template.id_chemical_samples = sampling  # Asocia cada plantilla con la instancia de ModelChemicalSampling
                template.save()

            messages.success(request, "El muestreo y las plantillas se han creado con éxito.")
            return redirect('sampling:feed')  # Redirigir a la página de feed después de guardar
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")

    else:
        # Si es GET, instanciamos los formularios vacíos
        sampling_form = SamplingForm()
        formset = TemplatesFormSet(queryset=ModelTemplates.objects.none())  # Creamos un formset vacío

    return render(request, 'sampling/create.html', {
        'sampling_form': sampling_form,
        'formset': formset,
        'user': request.user,
        'profile': request.user.profile
    })