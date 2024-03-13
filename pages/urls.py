from django.urls import path
from .views import homePageView, estadisticasPageView, VueloIndexView, VueloCreateView, VueloShowView


urlpatterns = [
    path("", homePageView.as_view(), name='home'),
    path('estadisticas/', estadisticasPageView.as_view(), name='estadisticas'),
    path('vuelos/', VueloIndexView.as_view(), name='index'),
    path('vuelos/create', VueloCreateView.as_view(), name='form'),
    path('vuelos/<str:id>', VueloShowView.as_view(), name='show'),
]
