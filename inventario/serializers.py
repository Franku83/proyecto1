from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import serializers

from .models import Proveedor, TipoJoya, Producto, Compra, Venta


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "telefono", "email"]


class TipoJoyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoJoya
        fields = ["id", "nombre"]


class ProductoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source="proveedor.nombre", read_only=True)
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = ["id", "nombre", "sku", "activo", "proveedor", "tipo", "proveedor_nombre", "tipo_nombre"]


class CompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    proveedor_id = serializers.IntegerField(source="producto.proveedor_id", read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "producto", "producto_nombre", "proveedor_id", "fecha", "cantidad", "precio_unitario"]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0.")
        return value

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio_unitario no puede ser negativo.")
        return value


class VentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    proveedor_id = serializers.IntegerField(source="producto.proveedor_id", read_only=True)

    class Meta:
        model = Venta
        fields = ["id", "producto", "producto_nombre", "proveedor_id", "fecha", "cantidad", "precio_unitario"]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0.")
        return value

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio_unitario no puede ser negativo.")
        return value

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
            raise serializers.ValidationError({"cantidad": f"No hay stock suficiente. Stock actual: {stock}."})

        return attrs