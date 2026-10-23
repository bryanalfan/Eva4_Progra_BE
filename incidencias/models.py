from django.db import models


class Categoria(models.Model):
    nombre = models.CharField("Nombre", max_length=60, unique=True)
    descripcion = models.CharField("Descripción", max_length=255, blank=True)
    habilitado = models.BooleanField("Habilitado", default=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría turística"
        verbose_name_plural = "categorías turísticas"
        db_table_comment = "Categorías de experiencias y paquetes turísticos."

    def __str__(self):
        return self.nombre


class Destino(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    ciudad = models.CharField("Ciudad", max_length=100)
    pais = models.CharField("País", max_length=100)
    descripcion = models.TextField("Descripción")
    mejor_epoca = models.CharField("Mejor época para visitar", max_length=100, blank=True)
    habilitado = models.BooleanField("Habilitado", default=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["pais", "ciudad", "nombre"]
        verbose_name = "destino"
        verbose_name_plural = "destinos"
        db_table_comment = "Destinos disponibles para visitar."
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "ciudad", "pais"], name="destino_lugar_unico"
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.ciudad}, {self.pais})"


class Viajero(models.Model):
    nombre = models.CharField("Nombre completo", max_length=150)
    correo = models.EmailField("Correo electrónico", unique=True)
    telefono = models.CharField("Teléfono", max_length=20, blank=True)
    nacionalidad = models.CharField("Nacionalidad", max_length=60, blank=True)
    created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "viajero"
        verbose_name_plural = "viajeros"
        db_table_comment = "Personas que reservan paquetes turísticos."

    def __str__(self):
        return self.nombre


class PaqueteTuristico(models.Model):
    nombre = models.CharField("Nombre", max_length=150)
    descripcion = models.TextField("Descripción")
    destino = models.ForeignKey(
        Destino,
        on_delete=models.PROTECT,
        related_name="paquetes",
        verbose_name="Destino",
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="paquetes",
        verbose_name="Categoría",
    )
    precio = models.DecimalField("Precio por persona", max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveSmallIntegerField("Duración (días)")
    max_personas = models.PositiveSmallIntegerField("Máximo de personas por reserva")
    habilitado = models.BooleanField("Habilitado", default=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "paquete turístico"
        verbose_name_plural = "paquetes turísticos"
        db_table_comment = "Experiencias y paquetes turísticos ofrecidos en un destino."

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    viajero = models.ForeignKey(
        Viajero,
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Viajero",
    )
    paquete = models.ForeignKey(
        PaqueteTuristico,
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Paquete turístico",
    )
    fecha_inicio = models.DateField("Fecha de inicio del viaje")
    cantidad_personas = models.PositiveSmallIntegerField("Cantidad de personas")
    precio_total = models.DecimalField(
        "Precio total", max_digits=12, decimal_places=2, editable=False
    )
    estado = models.CharField(
        "Estado", max_length=12, choices=Estado.choices, default=Estado.PENDIENTE
    )
    created_at = models.DateTimeField("Fecha de reserva", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        db_table_comment = "Reservas de paquetes turísticos realizadas por viajeros."

    def save(self, *args, **kwargs):
        if kwargs.get("raw", False):
            return super().save(*args, **kwargs)
        recalcular_precio = self._state.adding
        if not recalcular_precio:
            anterior = type(self).objects.only("paquete_id", "cantidad_personas").get(pk=self.pk)
            recalcular_precio = (
                self.paquete_id != anterior.paquete_id
                or self.cantidad_personas != anterior.cantidad_personas
            )
        if recalcular_precio:
            self.precio_total = self.paquete.precio * self.cantidad_personas
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"precio_total"}
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva #{self.pk} - {self.paquete}"


class Resena(models.Model):
    destino = models.ForeignKey(
        Destino,
        on_delete=models.CASCADE,
        related_name="resenas",
        verbose_name="Destino",
    )
    viajero = models.ForeignKey(
        Viajero,
        on_delete=models.PROTECT,
        related_name="resenas",
        verbose_name="Viajero",
    )
    puntuacion = models.PositiveSmallIntegerField("Puntuación (1 a 5)")
    comentario = models.TextField("Comentario")
    created_at = models.DateTimeField("Fecha de publicación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        db_table_comment = "Opiniones de viajeros sobre destinos turísticos."
        constraints = [
            models.UniqueConstraint(
                fields=["destino", "viajero"], name="resena_destino_viajero_unica"
            ),
            models.CheckConstraint(
                condition=models.Q(puntuacion__gte=1, puntuacion__lte=5),
                name="resena_rating_1_5",
            ),
        ]

    def __str__(self):
        return f"{self.destino} - {self.puntuacion}/5"
