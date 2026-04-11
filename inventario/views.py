from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Proveedor, TipoJoya, Producto, Compra, Venta, Cliente
from .serializers import (
    ProveedorSerializer, TipoJoyaSerializer, ProductoSerializer, 
    CompraSerializer, VentaSerializer, ClienteSerializer
)
from .utils import GroqClient

# --- Base Views ---

class ProveedorListCreateAPIView(APIView):
    def get(self, request):
        qs = Proveedor.objects.all()
        return Response(ProveedorSerializer(qs, many=True).data)

    def post(self, request):
        ser = ProveedorSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoListCreateAPIView(APIView):
    def get(self, request):
        qs = Producto.objects.select_related("proveedor", "tipo").all()
        return Response(ProductoSerializer(qs, many=True).data)

    def post(self, request):
        ser = ProductoSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ClienteListCreateAPIView(APIView):
    def get(self, request):
        qs = Cliente.objects.all()
        return Response(ClienteSerializer(qs, many=True).data)

    def post(self, request):
        ser = ClienteSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ClienteDetailAPIView(APIView):
    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        return Response(ClienteSerializer(cliente).data)

    def put(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        ser = ClienteSerializer(cliente, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

# --- AI Endpoints ---

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
