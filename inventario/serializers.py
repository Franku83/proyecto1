from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import serializers
from .models import Proveedor, TipoJoya, Producto, Compra, Venta, Cliente

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "telefono", "email"]

class TipoJoyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoJoya
        fields = ["id", "nombre"]

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "email", "telefono", "deuda_pendiente", "limite_credito"]

class ProductoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source="proveedor.nombre", read_only=True)
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id", "nombre", "sku", "activo", "proveedor", "tipo", 
            "proveedor_nombre", "tipo_nombre", "costo", "precio_venta", 
            "material", "descripcion_marketing"
        ]

class CompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "producto", "producto_nombre", "fecha", "cantidad", "precio_unitario"]

class VentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    cliente_nombre = serializers.CharField(source="cliente.nombre", read_only=True)

    class Meta:
        model = Venta
        fields = ["id", "producto", "producto_nombre", "cliente", "cliente_nombre", "fecha", "cantidad", "precio_unitario"]

    def validate(self, attrs):
        producto = attrs.get("producto") or getattr(self.instance, "producto", None)
        cantidad_nueva = attrs.get("cantidad") or getattr(self.instance, "cantidad", None)
        if not producto or not cantidad_nueva:
            return attrs

        compras_sum = producto.compras.aggregate(total=Coalesce(Sum("cantidad"), Value(0)))["total"]
        ventas_qs = producto.ventas.all()
        if self.instance:
            ventas_qs = ventas_qs.exclude(id=self.instance.id)
        ventas_sum = ventas_qs.aggregate(total=Coalesce(Sum("cantidad"), Value(0)))["total"]
        
        stock = int(compras_sum) - int(ventas_sum)
        if cantidad_nueva > stock:
            raise serializers.ValidationError({"cantidad": f"Stock insuficiente. Disponible: {stock}"})
        return attrs
