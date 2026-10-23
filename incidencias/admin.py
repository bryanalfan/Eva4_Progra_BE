from django.contrib import admin

from .models import Categoria, Destino, PaqueteTuristico, Reserva, Resena, Viajero


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "habilitado")
    list_filter = ("habilitado",)
    search_fields = ("nombre",)


@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "ciudad", "pais", "habilitado")
    list_filter = ("pais", "habilitado")
    search_fields = ("nombre", "ciudad", "pais")


@admin.register(Viajero)
class ViajeroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "correo", "telefono", "nacionalidad")
    search_fields = ("nombre", "correo", "nacionalidad")


@admin.register(PaqueteTuristico)
class PaqueteTuristicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "destino", "categoria", "precio", "duracion_dias", "habilitado")
    list_filter = ("categoria", "destino__pais", "habilitado")
    search_fields = ("nombre", "destino__nombre")


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "viajero", "paquete", "fecha_inicio", "cantidad_personas", "estado")
    list_filter = ("estado", "fecha_inicio")
    search_fields = ("viajero__nombre", "paquete__nombre")
    readonly_fields = ("precio_total", "created_at", "updated_at")


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ("id", "destino", "viajero", "puntuacion", "created_at")
    list_filter = ("puntuacion", "destino")
    search_fields = ("destino__nombre", "viajero__nombre", "comentario")
