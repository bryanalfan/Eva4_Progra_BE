from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Destino, PaqueteTuristico, Reserva, Resena


class PaginasHTMLTests(TestCase):
    fixtures = ["datos_turisticos"]

    def test_pagina_de_inicio_muestra_resumen_turistico(self):
        response = self.client.get(reverse("bienvenida"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bienvenida.html")
        self.assertEqual(response.context["cantidad_destinos"], 3)
        self.assertEqual(response.context["cantidad_paquetes"], 3)
        self.assertEqual(response.context["reservas_confirmadas"], 1)

    def test_pagina_404_personalizada(self):
        response = self.client.get("/ruta-que-no-existe/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Página no encontrada", status_code=404)


class CrudTodosLosModelosTests(APITestCase):
    """Verifica GET, POST, PUT, PATCH y DELETE en todos los recursos."""

    fixtures = ["datos_turisticos"]

    CASOS = {
        "categoria": (
            {"nombre": "Gastronomía"},
            {"descripcion": "Sabores y cocina local"},
        ),
        "destino": (
            {
                "nombre": "Valparaíso",
                "ciudad": "Valparaíso",
                "pais": "Chile",
                "descripcion": "Ciudad portuaria y cultural.",
            },
            {"mejor_epoca": "Todo el año"},
        ),
        "viajero": (
            {
                "nombre": "Luis Mora",
                "correo": "luis@ejemplo.cl",
                "nacionalidad": "Chilena",
            },
            {"telefono": "+56944444444"},
        ),
        "paqueteturistico": (
            {
                "nombre": "Ruta costera",
                "descripcion": "Recorrido por la costa.",
                "destino": 3,
                "categoria": 2,
                "precio": "120000.00",
                "duracion_dias": 2,
                "max_personas": 5,
            },
            {"precio": "125000.00"},
        ),
        "reserva": (
            {
                "viajero": 3,
                "paquete": 3,
                "fecha_inicio": "2027-03-10",
                "cantidad_personas": 2,
                "estado": "pendiente",
            },
            {"estado": "confirmada"},
        ),
        "resena": (
            {
                "destino": 3,
                "viajero": 1,
                "puntuacion": 5,
                "comentario": "Un viaje maravilloso.",
            },
            {"comentario": "Una experiencia maravillosa."},
        ),
    }

    def test_crud_completo(self):
        for basename, (datos, parcial) in self.CASOS.items():
            with self.subTest(recurso=basename):
                url_lista = reverse(f"{basename}-list")

                response = self.client.get(url_lista)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                response = self.client.post(url_lista, datos, format="json")
                self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
                url_detalle = reverse(f"{basename}-detail", args=[response.data["id"]])

                response = self.client.get(url_detalle)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                response = self.client.put(url_detalle, datos, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

                response = self.client.patch(url_detalle, parcial, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
                for campo, valor in parcial.items():
                    self.assertEqual(response.data[campo], valor)

                response = self.client.delete(url_detalle)
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertEqual(self.client.get(url_detalle).status_code, status.HTTP_404_NOT_FOUND)


class ViajesReglasTests(APITestCase):
    fixtures = ["datos_turisticos"]

    def test_filtrar_destinos_por_pais(self):
        response = self.client.get(reverse("destino-list"), {"pais": "chile"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filtrar_paquetes_por_destino(self):
        response = self.client.get(reverse("paqueteturistico-list"), {"destino": 2})
        self.assertEqual([paquete["id"] for paquete in response.data], [2])

    def test_reserva_calcula_precio_total(self):
        response = self.client.post(
            reverse("reserva-list"),
            {
                "viajero": 3,
                "paquete": 1,
                "fecha_inicio": "2027-04-01",
                "cantidad_personas": 3,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["precio_total"], "2385000.00")

    def test_reserva_no_supera_capacidad_del_paquete(self):
        response = self.client.post(
            reverse("reserva-list"),
            {
                "viajero": 3,
                "paquete": 1,
                "fecha_inicio": "2027-04-01",
                "cantidad_personas": 9,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_precio_total_cambia_si_se_modifica_la_cantidad(self):
        reserva = Reserva.objects.get(pk=1)
        reserva.cantidad_personas = 3
        reserva.save(update_fields=["cantidad_personas"])
        reserva.refresh_from_db()
        self.assertEqual(reserva.precio_total, Decimal("2385000.00"))

    def test_puntuacion_de_resena_debe_estar_entre_uno_y_cinco(self):
        response = self.client.post(
            reverse("resena-list"),
            {
                "destino": 3,
                "viajero": 1,
                "puntuacion": 6,
                "comentario": "Puntuación no válida.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_viajero_no_puede_repetir_resena_para_el_destino(self):
        response = self.client.post(
            reverse("resena-list"),
            {
                "destino": 1,
                "viajero": 2,
                "puntuacion": 5,
                "comentario": "Otra opinión del mismo destino.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_se_elimina_destino_con_paquetes(self):
        response = self.client.delete(reverse("destino-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Destino.objects.filter(pk=1).exists())

    def test_eliminar_destino_elimina_sus_resenas(self):
        destino = Destino.objects.create(
            nombre="Destino temporal",
            ciudad="Ciudad temporal",
            pais="Chile",
            descripcion="Destino de prueba.",
        )
        Resena.objects.create(
            destino=destino,
            viajero_id=3,
            puntuacion=4,
            comentario="Buena experiencia.",
        )
        response = self.client.delete(reverse("destino-detail", args=[destino.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Resena.objects.filter(destino=destino).exists())

    def test_categoria_en_uso_no_se_elimina(self):
        response = self.client.delete(reverse("categoria-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Categoria.objects.filter(pk=1).exists())

    def test_paquete_con_reserva_no_se_elimina(self):
        response = self.client.delete(reverse("paqueteturistico-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(PaqueteTuristico.objects.filter(pk=1).exists())

    def test_viajero_con_reserva_no_se_elimina(self):
        response = self.client.delete(reverse("viajero-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Reserva.objects.filter(viajero_id=1).exists())
