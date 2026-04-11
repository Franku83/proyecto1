from django.contrib import admin
from django.urls import path
from inventario.views import (
    ProveedorListCreateAPIView, ProductoListCreateAPIView,
    ClienteListCreateAPIView, ClienteDetailAPIView,
    GenerarMarketingAPIView, SugerirPrecioAPIView, AnalisisRiesgoClienteAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inventario
    path('proveedores/', ProveedorListCreateAPIView.as_view(), name='proveedor-list'),
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list'),
    
    # Clientes
    path('clientes/', ClienteListCreateAPIView.as_view(), name='cliente-list'),
    path('clientes/<int:pk>/', ClienteDetailAPIView.as_view(), name='cliente-detail'),

    # IA (Groq)
    path('productos/<int:pk>/generar-marketing/', GenerarMarketingAPIView.as_view(), name='generar-marketing'),
    path('productos/<int:pk>/sugerir-precio/', SugerirPrecioAPIView.as_view(), name='sugerir-precio'),
    path('clientes/<int:pk>/analisis-riesgo/', AnalisisRiesgoClienteAPIView.as_view(), name='analisis-riesgo'),
]
