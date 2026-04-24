# Joyería API Inteligente 💎

API REST profesional para la gestión de inventarios, compras y ventas de joyería, potenciada con Inteligencia Artificial (Llama 3 via Groq).

## 🚀 Características Principales

- **Gestión Completa de Inventario:** Control de productos, proveedores, categorías (tipos), compras y ventas.
- **Lógica de Stock Inteligente:** Validación automática de existencias. No permite ventas si no hay stock disponible.
- **Integración con IA (Groq):**
  - Generación automática de descripciones de marketing.
  - Sugerencia de precios de venta basada en costos y materiales.
  - Análisis de riesgo crediticio para clientes.
- **Seguridad Robustecida:** 
  - Autenticación mediante `X-API-Key` personalizada.
  - Protección contra Inyección de Prompts en la IA.
  - Usuarios virtuales autenticados para operaciones de escritura.

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.x, Django 5.x, Django Rest Framework (DRF).
- **IA:** Groq Cloud SDK (Llama 3.3 70B).
- **Base de Datos:** PostgreSQL (Producción) / SQLite (Desarrollo).
- **Despliegue:** Railway.
- **Seguridad:** CORS Headers, WhiteNoise, API Key Auth.

## 🔑 Configuración de Variables de Entorno

Para que el proyecto funcione correctamente, configura las siguientes variables en tu archivo `.env` o en el panel de Railway:

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta
API_KEY=tu_clave_para_yaak_o_postman
GROQ_API_KEY=tu_api_key_de_groq
DATABASE_URL=url_de_tu_base_de_datos
```

## 📍 Endpoints Principales

### Inventario
- `GET /productos/` - Lista todos los productos.
- `POST /productos/` - Crea un nuevo producto (Requiere API Key).
- `GET /tipos/` - Categorías de joyas (Anillos, Collares, etc).

### Movimientos
- `POST /compras/` - Registra entrada de mercancía.
- `POST /ventas/` - Registra salida (Valida stock).

### Inteligencia Artificial (POST)
- `/productos/{id}/generar-marketing/` - Crea texto publicitario.
- `/productos/{id}/sugerir-precio/` - Calcula precio sugerido.
- `/clientes/{id}/analisis-riesgo/` - Evalúa si el cliente es apto para crédito.

---
*Proyecto desarrollado para exposición técnica de API REST e Integración de IA.*
