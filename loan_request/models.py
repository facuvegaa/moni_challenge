"""Loan request app Models."""
from django.db import models


class LoanRequest(models.Model):
    """Modelo Loan Request."""

    dni = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    genero = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    monto_solicitado = models.PositiveIntegerField(default=1000)
    aprobado = models.BooleanField(default=False)
    respuesta_api = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Representacion del modelo."""
        return f"{self.nombre} {self.apellido}"
