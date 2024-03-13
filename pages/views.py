from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Vuelo
from django.db.models import Count, Avg




# Create your views here.
class homePageView(TemplateView):
    template_name = 'home.html'

class estadisticasPageView(TemplateView):
    template_name = 'pages/estadisticas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la cantidad de vuelos nacionales e internacionales
        vuelos_nacionales = Vuelo.objects.filter(tipo='Nacional').count()
        vuelos_internacionales = Vuelo.objects.filter(tipo='Internacional').count()

        # Obtener el precio promedio de los vuelos nacionales
        precio_promedio_nacionales = Vuelo.objects.filter(tipo='Nacional').aggregate(Avg('price'))['price__avg']

        # Si no hay vuelos nacionales, establece el precio promedio a 0
        if precio_promedio_nacionales is None:
            precio_promedio_nacionales = 0

        context['vuelos_nacionales'] = vuelos_nacionales
        context['vuelos_internacionales'] = vuelos_internacionales
        context['precio_promedio_nacionales'] = precio_promedio_nacionales

        return context

class VueloIndexView(ListView):
    template_name = 'vuelos/index.html'
    context_object_name = 'vuelos'  # Este nombre se utilizará en la plantilla HTML para iterar sobre los vuelos

    def get_queryset(self):
        return Vuelo.objects.order_by('price')  # Ordena los vuelos por precio


class VueloShowView(View):
    template_name = 'vuelos/show.html'


    def get(self, request, id):

        # Check if product id is valid
        try:
            id_vuelo = int(id)
            if id_vuelo < 1:
                raise ValueError("no hay vuelos")
            vuelo = get_object_or_404(Vuelo, pk=id_vuelo)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        vuelo = get_object_or_404(Vuelo, pk=id_vuelo)
        viewData["title"] = vuelo.name + " - Online Store"
        viewData["subtitle"] =  vuelo.name + " - informacion del Vuelo"
        viewData["vuelo"] = vuelo

        return render(request, self.template_name, viewData)


class VueloListView(ListView):
    model = Vuelo
    template_name = 'vuelo_list.html'
    context_object_name = 'vuelos'  # This will allow you to loop through 'vuelos' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vuelos Disponibles'
        context['subtitle'] = 'Listado de Vuelos'
        return context   

class VueloForm(forms.ModelForm):
    class Meta:
        model=Vuelo
        fields=['name','price','tipo']
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

class VueloCreateView(View):
    template_name = 'vuelos/create.html'

    def get(self, request):
        form = VueloForm()
        viewData = {}
        viewData["title"] = "Registrar Vuelos"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = VueloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('form') 
        else:
            viewData = {}
            viewData["title"] = "Registrar Vuelo"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
