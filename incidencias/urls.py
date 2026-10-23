from django.urls import include, path
from rest_framework import routers

from incidencias import views

enrutador = routers.DefaultRouter()

enrutador.register(r"categorias", views.CategoriaViewSet)
enrutador.register(r"destinos", views.DestinoViewSet)
enrutador.register(r"viajeros", views.ViajeroViewSet)
enrutador.register(r"paquetes", views.PaqueteTuristicoViewSet)
enrutador.register(r"reservas", views.ReservaViewSet)
enrutador.register(r"resenas", views.ResenaViewSet)

urlpatterns = [
    path("", include(enrutador.urls)),
]
