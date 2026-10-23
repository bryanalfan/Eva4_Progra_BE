import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incidencias", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Comentario"),
        migrations.DeleteModel(name="Incidencia"),
        migrations.DeleteModel(name="Usuario"),
        migrations.DeleteModel(name="Estado"),
        migrations.DeleteModel(name="Prioridad"),
        migrations.DeleteModel(name="Departamento"),
        migrations.DeleteModel(name="Categoria"),
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=60, unique=True, verbose_name="Nombre")),
                ("descripcion", models.CharField(blank=True, max_length=255, verbose_name="Descripción")),
                ("habilitado", models.BooleanField(default=True, verbose_name="Habilitado")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
            ],
            options={
                "verbose_name": "categoría turística",
                "verbose_name_plural": "categorías turísticas",
                "db_table_comment": "Categorías de experiencias y paquetes turísticos.",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Destino",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, verbose_name="Nombre")),
                ("ciudad", models.CharField(max_length=100, verbose_name="Ciudad")),
                ("pais", models.CharField(max_length=100, verbose_name="País")),
                ("descripcion", models.TextField(verbose_name="Descripción")),
                ("mejor_epoca", models.CharField(blank=True, max_length=100, verbose_name="Mejor época para visitar")),
                ("habilitado", models.BooleanField(default=True, verbose_name="Habilitado")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
            ],
            options={
                "verbose_name": "destino",
                "verbose_name_plural": "destinos",
                "db_table_comment": "Destinos disponibles para visitar.",
                "ordering": ["pais", "ciudad", "nombre"],
            },
        ),
        migrations.CreateModel(
            name="Viajero",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150, verbose_name="Nombre completo")),
                ("correo", models.EmailField(max_length=254, unique=True, verbose_name="Correo electrónico")),
                ("telefono", models.CharField(blank=True, max_length=20, verbose_name="Teléfono")),
                ("nacionalidad", models.CharField(blank=True, max_length=60, verbose_name="Nacionalidad")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
            ],
            options={
                "verbose_name": "viajero",
                "verbose_name_plural": "viajeros",
                "db_table_comment": "Personas que reservan paquetes turísticos.",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="PaqueteTuristico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150, verbose_name="Nombre")),
                ("descripcion", models.TextField(verbose_name="Descripción")),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Precio por persona")),
                ("duracion_dias", models.PositiveSmallIntegerField(verbose_name="Duración (días)")),
                ("max_personas", models.PositiveSmallIntegerField(verbose_name="Máximo de personas por reserva")),
                ("habilitado", models.BooleanField(default=True, verbose_name="Habilitado")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="paquetes", to="incidencias.categoria", verbose_name="Categoría")),
                ("destino", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="paquetes", to="incidencias.destino", verbose_name="Destino")),
            ],
            options={
                "verbose_name": "paquete turístico",
                "verbose_name_plural": "paquetes turísticos",
                "db_table_comment": "Experiencias y paquetes turísticos ofrecidos en un destino.",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Reserva",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_inicio", models.DateField(verbose_name="Fecha de inicio del viaje")),
                ("cantidad_personas", models.PositiveSmallIntegerField(verbose_name="Cantidad de personas")),
                ("precio_total", models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name="Precio total")),
                ("estado", models.CharField(choices=[("pendiente", "Pendiente"), ("confirmada", "Confirmada"), ("cancelada", "Cancelada")], default="pendiente", max_length=12, verbose_name="Estado")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de reserva")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("paquete", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservas", to="incidencias.paqueteturistico", verbose_name="Paquete turístico")),
                ("viajero", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservas", to="incidencias.viajero", verbose_name="Viajero")),
            ],
            options={
                "verbose_name": "reserva",
                "verbose_name_plural": "reservas",
                "db_table_comment": "Reservas de paquetes turísticos realizadas por viajeros.",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Resena",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("puntuacion", models.PositiveSmallIntegerField(verbose_name="Puntuación (1 a 5)")),
                ("comentario", models.TextField(verbose_name="Comentario")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("destino", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resenas", to="incidencias.destino", verbose_name="Destino")),
                ("viajero", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="resenas", to="incidencias.viajero", verbose_name="Viajero")),
            ],
            options={
                "verbose_name": "reseña",
                "verbose_name_plural": "reseñas",
                "db_table_comment": "Opiniones de viajeros sobre destinos turísticos.",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="destino",
            constraint=models.UniqueConstraint(fields=("nombre", "ciudad", "pais"), name="destino_lugar_unico"),
        ),
        migrations.AddConstraint(
            model_name="resena",
            constraint=models.UniqueConstraint(fields=("destino", "viajero"), name="resena_destino_viajero_unica"),
        ),
        migrations.AddConstraint(
            model_name="resena",
            constraint=models.CheckConstraint(condition=models.Q(("puntuacion__gte", 1), ("puntuacion__lte", 5)), name="resena_rating_1_5"),
        ),
    ]
