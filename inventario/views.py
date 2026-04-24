from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Proveedor, Producto, Cliente, TipoJoya, Compra, Venta
from .serializers import (
    ProveedorSerializer, ProductoSerializer, ClienteSerializer,
    TipoJoyaSerializer, CompraSerializer, VentaSerializer
)
from .utils import GroqClient

class ProveedorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class TipoJoyaListCreateAPIView(generics.ListCreateAPIView):
    queryset = TipoJoya.objects.all()
    serializer_class = TipoJoyaSerializer

class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.select_related("proveedor", "tipo").all()
    serializer_class = ProductoSerializer

class ClienteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class CompraListCreateAPIView(generics.ListCreateAPIView):
    queryset = Compra.objects.select_related("producto").all()
    serializer_class = CompraSerializer

class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.select_related("producto", "cliente").all()
    serializer_class = VentaSerializer

class GenerarMarketingAPIView(APIView):
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        client = GroqClient()
        descripcion = client.generar_marketing(producto.nombre, producto.material)
        producto.descripcion_marketing = descripcion
        producto.save()
        return Response({"id": producto.id, "descripcion_marketing": descripcion})

class SugerirPrecioAPIView(APIView):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        client = GroqClient()
        sugerencia = client.sugerir_precio(producto.nombre, producto.material, producto.costo)
        return Response({"id": producto.id, "sugerencia_ia": sugerencia})

class AnalisisRiesgoClienteAPIView(APIView):
    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        client = GroqClient()
        analisis = client.analizar_riesgo(cliente.nombre, cliente.deuda_pendiente, cliente.limite_credito)
        return Response({"id": cliente.id, "analisis_riesgo": analisis})
