from django.db.models import ProtectedError
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Categoria, Destino, PaqueteTuristico, Reserva, Resena, Viajero
from .serializers import (
    CategoriaSerializer,
    DestinoSerializer,
    PaqueteTuristicoSerializer,
    ReservaSerializer,
    ResenaSerializer,
    ViajeroSerializer,
)


def bienvenida(request):
    """Página principal con un resumen de la oferta turística."""
    contexto = {
        "cantidad_destinos": Destino.objects.filter(habilitado=True).count(),
        "cantidad_paquetes": PaqueteTuristico.objects.filter(habilitado=True).count(),
        "reservas_confirmadas": Reserva.objects.filter(
            estado=Reserva.Estado.CONFIRMADA
        ).count(),
        "fecha_consulta": timezone.localtime().strftime("%d/%m/%Y %H:%M"),
    }
    return render(request, "bienvenida.html", contexto)


def error_404(request, exception):
    """Muestra una página personalizada cuando la URL no existe."""
    return render(request, "404.html", status=404)


class ProtegidoViewSet(viewsets.ModelViewSet):
    """Devuelve 409 cuando no se puede eliminar un registro que está en uso."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar: existen registros que dependen de este."},
                status=status.HTTP_409_CONFLICT,
            )


class CategoriaViewSet(ProtegidoViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class DestinoViewSet(ProtegidoViewSet):
    queryset = Destino.objects.all()
    serializer_class = DestinoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        for campo in ("pais", "ciudad"):
            valor = self.request.query_params.get(campo)
            if valor:
                queryset = queryset.filter(**{f"{campo}__icontains": valor})
        return queryset


class ViajeroViewSet(ProtegidoViewSet):
    queryset = Viajero.objects.all()
    serializer_class = ViajeroSerializer


class PaqueteTuristicoViewSet(ProtegidoViewSet):
    queryset = PaqueteTuristico.objects.select_related("destino", "categoria")
    serializer_class = PaqueteTuristicoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        for campo in ("destino", "categoria"):
            valor = self.request.query_params.get(campo)
            if valor:
                queryset = queryset.filter(**{campo: valor})
        return queryset


class ReservaViewSet(ProtegidoViewSet):
    queryset = Reserva.objects.select_related("viajero", "paquete")
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        for campo in ("viajero", "estado"):
            valor = self.request.query_params.get(campo)
            if valor:
                queryset = queryset.filter(**{campo: valor})
        return queryset


class ResenaViewSet(ProtegidoViewSet):
    queryset = Resena.objects.select_related("destino", "viajero")
    serializer_class = ResenaSerializer
