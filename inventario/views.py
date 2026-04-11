from django.db.models import Sum, Value, F
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Proveedor, TipoJoya, Producto, Compra, Venta
from .serializers import (
    ProveedorSerializer,
    TipoJoyaSerializer,
    ProductoSerializer,
    CompraSerializer,
    VentaSerializer,
)


def parse_bool_int(value: str) -> bool:
    return str(value).strip() in ("1", "true", "True", "yes", "YES")


class BaseDetailAPIView(APIView):
    model = None
    serializer_class = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None


class ProveedorListCreateAPIView(APIView):
    def get(self, request):
        qs = Proveedor.objects.all().order_by("nombre")
        return Response(ProveedorSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = ProveedorSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            return Response(ProveedorSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorDetailAPIView(BaseDetailAPIView):
    model = Proveedor
    serializer_class = ProveedorSerializer

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data)
        if ser.is_valid():
            obj = ser.save()
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data, partial=True)
        if ser.is_valid():
            obj = ser.save()
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TipoJoyaListCreateAPIView(APIView):
    def get(self, request):
        qs = TipoJoya.objects.all().order_by("nombre")
        return Response(TipoJoyaSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = TipoJoyaSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            return Response(TipoJoyaSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class TipoJoyaDetailAPIView(BaseDetailAPIView):
    model = TipoJoya
    serializer_class = TipoJoyaSerializer

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data)
        if ser.is_valid():
            obj = ser.save()
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data, partial=True)
        if ser.is_valid():
            obj = ser.save()
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductoListCreateAPIView(APIView):
    def get(self, request):
        qs = Producto.objects.select_related("proveedor", "tipo").all().order_by("nombre")

        proveedor = request.query_params.get("proveedor")
        tipo = request.query_params.get("tipo")
        q = request.query_params.get("q")
        solo_stock = request.query_params.get("solo_stock")

        if proveedor:
            qs = qs.filter(proveedor_id=proveedor)
        if tipo:
            qs = qs.filter(tipo_id=tipo)
        if q:
            qs = qs.filter(nombre__icontains=q)

        if solo_stock is not None and parse_bool_int(solo_stock):
            qs = qs.annotate(
                compras_total=Coalesce(Sum("compras__cantidad"), Value(0)),
                ventas_total=Coalesce(Sum("ventas__cantidad"), Value(0)),
            ).annotate(stock=F("compras_total") - F("ventas_total")).filter(stock__gt=0)

        return Response(ProductoSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = ProductoSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Producto.objects.select_related("proveedor", "tipo").get(id=obj.id)
            return Response(ProductoSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetailAPIView(BaseDetailAPIView):
    model = Producto
    serializer_class = ProductoSerializer

    def get(self, request, pk):
        obj = Producto.objects.select_related("proveedor", "tipo").filter(pk=pk).first()
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Producto.objects.select_related("proveedor", "tipo").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data, partial=True)
        if ser.is_valid():
            obj = ser.save()
            obj = Producto.objects.select_related("proveedor", "tipo").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompraListCreateAPIView(APIView):
    def get(self, request):
        qs = Compra.objects.select_related("producto", "producto__proveedor").all().order_by("-fecha", "-id")

        producto = request.query_params.get("producto")
        proveedor = request.query_params.get("proveedor")
        desde = request.query_params.get("desde")
        hasta = request.query_params.get("hasta")

        if producto:
            qs = qs.filter(producto_id=producto)
        if proveedor:
            qs = qs.filter(producto__proveedor_id=proveedor)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)

        return Response(CompraSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = CompraSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Compra.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(CompraSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class CompraDetailAPIView(BaseDetailAPIView):
    model = Compra
    serializer_class = CompraSerializer

    def get(self, request, pk):
        obj = Compra.objects.select_related("producto", "producto__proveedor").filter(pk=pk).first()
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Compra.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data, partial=True)
        if ser.is_valid():
            obj = ser.save()
            obj = Compra.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VentaListCreateAPIView(APIView):
    def get(self, request):
        qs = Venta.objects.select_related("producto", "producto__proveedor").all().order_by("-fecha", "-id")

        producto = request.query_params.get("producto")
        proveedor = request.query_params.get("proveedor")
        desde = request.query_params.get("desde")
        hasta = request.query_params.get("hasta")

        if producto:
            qs = qs.filter(producto_id=producto)
        if proveedor:
            qs = qs.filter(producto__proveedor_id=proveedor)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)

        return Response(VentaSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = VentaSerializer(data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Venta.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(VentaSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaDetailAPIView(BaseDetailAPIView):
    model = Venta
    serializer_class = VentaSerializer

    def get(self, request, pk):
        obj = Venta.objects.select_related("producto", "producto__proveedor").filter(pk=pk).first()
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data)
        if ser.is_valid():
            obj = ser.save()
            obj = Venta.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(obj, data=request.data, partial=True)
        if ser.is_valid():
            obj = ser.save()
            obj = Venta.objects.select_related("producto", "producto__proveedor").get(id=obj.id)
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InventarioAPIView(APIView):
    def get(self, request):
        qs = (
            Producto.objects.select_related("proveedor", "tipo")
            .all()
            .annotate(
                compras_total=Coalesce(Sum("compras__cantidad"), Value(0)),
                ventas_total=Coalesce(Sum("ventas__cantidad"), Value(0)),
            )
            .annotate(stock=F("compras_total") - F("ventas_total"))
            .order_by("nombre")
        )

        proveedor = request.query_params.get("proveedor")
        tipo = request.query_params.get("tipo")
        q = request.query_params.get("q")
        solo_stock = request.query_params.get("solo_stock")

        if proveedor:
            qs = qs.filter(proveedor_id=proveedor)
        if tipo:
            qs = qs.filter(tipo_id=tipo)
        if q:
            qs = qs.filter(nombre__icontains=q)
        if solo_stock is not None and parse_bool_int(solo_stock):
            qs = qs.filter(stock__gt=0)

        data = [
            {
                "producto_id": p.id,
                "producto": p.nombre,
                "proveedor_id": p.proveedor_id,
                "proveedor": p.proveedor.nombre,
                "tipo_id": p.tipo_id,
                "tipo": p.tipo.nombre,
                "stock": int(p.stock),
            }
            for p in qs
        ]
        return Response(data, status=status.HTTP_200_OK)