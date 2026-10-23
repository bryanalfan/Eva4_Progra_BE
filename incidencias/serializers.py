from rest_framework import serializers

from .models import Categoria, Destino, PaqueteTuristico, Reserva, Resena, Viajero


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = "__all__"


class ViajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viajero
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class PaqueteTuristicoSerializer(serializers.ModelSerializer):
    destino_nombre = serializers.CharField(source="destino.nombre", read_only=True)
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = PaqueteTuristico
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        precio = attrs.get("precio", getattr(self.instance, "precio", None))
        duracion = attrs.get("duracion_dias", getattr(self.instance, "duracion_dias", None))
        max_personas = attrs.get("max_personas", getattr(self.instance, "max_personas", None))
        if precio is not None and precio <= 0:
            raise serializers.ValidationError({"precio": "El precio debe ser mayor que cero."})
        if duracion is not None and duracion < 1:
            raise serializers.ValidationError({"duracion_dias": "La duración mínima es de un día."})
        if max_personas is not None and max_personas < 1:
            raise serializers.ValidationError(
                {"max_personas": "Debe permitirse al menos una persona por reserva."}
            )
        return attrs


class ReservaSerializer(serializers.ModelSerializer):
    viajero_nombre = serializers.CharField(source="viajero.nombre", read_only=True)
    paquete_nombre = serializers.CharField(source="paquete.nombre", read_only=True)

    class Meta:
        model = Reserva
        fields = "__all__"
        read_only_fields = ["precio_total", "created_at", "updated_at"]

    def validate(self, attrs):
        paquete = attrs.get("paquete", getattr(self.instance, "paquete", None))
        cantidad = attrs.get(
            "cantidad_personas", getattr(self.instance, "cantidad_personas", None)
        )
        if cantidad is not None and cantidad < 1:
            raise serializers.ValidationError(
                {"cantidad_personas": "La reserva debe incluir al menos una persona."}
            )
        if paquete is not None and cantidad is not None and cantidad > paquete.max_personas:
            raise serializers.ValidationError(
                {
                    "cantidad_personas": (
                        f"Este paquete admite hasta {paquete.max_personas} personas por reserva."
                    )
                }
            )
        return attrs

class ResenaSerializer(serializers.ModelSerializer):
    destino_nombre = serializers.CharField(source="destino.nombre", read_only=True)
    viajero_nombre = serializers.CharField(source="viajero.nombre", read_only=True)

    class Meta:
        model = Resena
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        destino = attrs.get("destino", getattr(self.instance, "destino", None))
        viajero = attrs.get("viajero", getattr(self.instance, "viajero", None))
        resenas_existentes = Resena.objects.filter(destino=destino, viajero=viajero)
        if self.instance is not None:
            resenas_existentes = resenas_existentes.exclude(pk=self.instance.pk)
        if resenas_existentes.exists():
            raise serializers.ValidationError(
                "Este viajero ya publicó una reseña para este destino."
            )
        return attrs

    def validate_puntuacion(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return value
