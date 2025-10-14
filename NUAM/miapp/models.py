from django.db import models
from django.contrib.auth.models import User

 

class Pais(models.Model):
    """Representa un país participante (Chile, Perú, Colombia)."""
    nombre = models.CharField(max_length=100, unique=True)
    codigo_iso = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre


class Moneda(models.Model):
    """Define las monedas utilizadas en los cálculos (CLP, PEN, COP, USD, etc.)."""
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} ({self.simbolo or ''})"


class Emisor(models.Model):
    """Entidad o empresa emisora a la que se asignan calificaciones tributarias."""
    nombre = models.CharField(max_length=150, unique=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, related_name="emisores")

    def __str__(self):
        return self.nombre


class CalificacionTributaria(models.Model):
    """Calificación tributaria asociada a un emisor."""
    emisor = models.ForeignKey(Emisor, on_delete=models.CASCADE, related_name="calificaciones")
    codigo_calificacion = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo_calificacion} - {self.emisor.nombre}"


class FactorConversion(models.Model):
    """Factores utilizados para convertir montos según reglas tributarias."""
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, related_name="factores_conversion")
    moneda_origen = models.ForeignKey(Moneda, on_delete=models.SET_NULL, null=True, related_name="conversiones_origen")
    moneda_destino = models.ForeignKey(Moneda, on_delete=models.SET_NULL, null=True, related_name="conversiones_destino")
    factor = models.DecimalField(max_digits=12, decimal_places=6)
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.moneda_origen.codigo} → {self.moneda_destino.codigo} ({self.factor})"


class ConversionMonto(models.Model):
    """Historial de conversiones de montos a factores tributarios."""
    fecha_conversion = models.DateTimeField(auto_now_add=True)
    monto_original = models.DecimalField(max_digits=18, decimal_places=2)
    factor_usado = models.ForeignKey(FactorConversion, on_delete=models.PROTECT, related_name="conversiones")
    monto_convertido = models.DecimalField(max_digits=18, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="conversiones_realizadas")

    def __str__(self):
        return f"Conversión {self.monto_original} → {self.monto_convertido}"


class BitacoraCambios(models.Model):
    """Registra cambios o modificaciones en calificaciones o factores."""
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    entidad_afectada = models.CharField(max_length=100)
    descripcion_cambio = models.TextField()

    def __str__(self):
        return f"{self.entidad_afectada} modificado por {self.usuario} en {self.fecha_modificacion}"
