from django.contrib import admin
from django.urls import path
from inventario.views import (
    ProveedorListCreateAPIView, ProductoListCreateAPIView,
    ClienteListCreateAPIView, ClienteDetailAPIView,
    TipoJoyaListCreateAPIView, CompraListCreateAPIView, VentaListCreateAPIView,
    GenerarMarketingAPIView, SugerirPrecioAPIView, AnalisisRiesgoClienteAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('proveedores/', ProveedorListCreateAPIView.as_view(), name='proveedor-list'),
    path('tipos/', TipoJoyaListCreateAPIView.as_view(), name='tipo-list'),
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list'),
    
    path('clientes/', ClienteListCreateAPIView.as_view(), name='cliente-list'),
    path('clientes/<int:pk>/', ClienteDetailAPIView.as_view(), name='cliente-detail'),

    path('compras/', CompraListCreateAPIView.as_view(), name='compra-list'),
    path('ventas/', VentaListCreateAPIView.as_view(), name='venta-list'),

    path('productos/<int:pk>/generar-marketing/', GenerarMarketingAPIView.as_view(), name='generar-marketing'),
    path('productos/<int:pk>/sugerir-precio/', SugerirPrecioAPIView.as_view(), name='sugerir-precio'),
    path('clientes/<int:pk>/analisis-riesgo/', AnalisisRiesgoClienteAPIView.as_view(), name='analisis-riesgo'),
]
