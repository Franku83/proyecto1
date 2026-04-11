from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    telefono = models.CharField(max_length=40, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return self.nombre

class TipoJoya(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="productos")
    tipo = models.ForeignKey(TipoJoya, on_delete=models.PROTECT, related_name="productos")
    sku = models.CharField(max_length=60, blank=True, default="")
    activo = models.BooleanField(default=True)
    # Nuevos campos
    costo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    material = models.CharField(max_length=100, blank=True, default="")
    descripcion_marketing = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ("nombre", "proveedor", "tipo")

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=40, blank=True, default="")
    deuda_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="compras")
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.id} - {self.producto.nombre}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="ventas")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ventas", null=True, blank=True)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.id} - {self.producto.nombre}"
