# Inventory Manager - Sistema Completo de Gestión de Inventario

## 📋 Descripción

Sistema completo de gestión de inventario desarrollado con **Python/FastAPI** (backend) y **JavaScript vanilla** (frontend). Incluye API RESTful robusta, interfaz web moderna y responsive, autenticación JWT, importación/exportación masiva de datos, y optimización para grandes volúmenes (+100k registros).

---

##  Características Principales

### 🔧 Backend (API)
- ✅ **API RESTful** con FastAPI
- ✅ **Autenticación JWT** segura
- ✅ **CRUD completo** de productos
- ✅ **Importación masiva** desde CSV/Excel con validación
- ✅ **Exportación optimizada** a CSV/Excel (+100k registros)
- ✅ **Sistema de auditoría** completo
- ✅ **Documentación automática** (Swagger/ReDoc)
- ✅ **Versionado de API** (v1)
- ✅ **Filtros avanzados** y búsqueda
- ✅ **Paginación** automática
- ✅ **Base de datos** PostgreSQL/SQLite

###  Frontend (Web UI)
- ✅ **Interfaz moderna** y responsive
- ✅ **Dashboard** con estadísticas en tiempo real
- ✅ **Gestión visual** de productos
- ✅ **Búsqueda y filtros** interactivos
- ✅ **Drag & drop** para importación
- ✅ **Exportación** con un click
- ✅ **Diseño responsive** (móvil, tablet, desktop)
- ✅ **Animaciones suaves**
- ✅ **Sin dependencias** (JavaScript vanilla)

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| FastAPI | 0.109.0 | Framework web |
| SQLAlchemy | 2.0.25 | ORM |
| Pydantic | 2.5.3 | Validación |
| JWT | - | Autenticación |
| Pandas | 2.1.4 | Procesamiento CSV/Excel |
| PostgreSQL | - | Base de datos (producción) |
| SQLite | - | Base de datos (desarrollo) |
| Uvicorn | 0.27.0 | Servidor ASGI |

### Frontend
| Tecnología | Uso |
|------------|-----|
| HTML5 | Estructura |
| CSS3 | Estilos modernos |
| JavaScript | Lógica (vanilla, sin frameworks) |
| Font Awesome | Iconos |
| Fetch API | Comunicación con backend |

---

## 📦 Instalación Completa

### Requisitos Previos

- **Python 3.10 o superior**
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para clonar)
- **PostgreSQL** (opcional, SQLite por defecto)

### Paso 1: Obtener el Proyecto

```bash
# Clonar desde repositorio (si aplica)
git clone https://github.com/Jefer526/Prueba_Api_Python
cd Prueba_Api_Python
```

### Paso 2: Configurar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

**Dependencias principales instaladas:**
- fastapi, uvicorn (framework y servidor)
- sqlalchemy, alembic (base de datos)
- python-jose, passlib, bcrypt (autenticación)
- pandas, openpyxl (procesamiento de archivos)
- pydantic, pydantic-settings (validación)

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar el archivo .env
# Windows: notepad .env
# Linux/Mac: nano .env
```

**Contenido de `.env` (desarrollo con SQLite):**

```env
# Database - SQLite para desarrollo
DATABASE_URL=sqlite:///./inventory.db

# JWT Security
SECRET_KEY=change-this-to-a-secure-random-string-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Inventory API
APP_VERSION=1.0.0
DEBUG=True

# CORS - Agregar tus dominios permitidos
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_FOLDER=./uploads

# Pagination
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=1000

# Export
MAX_EXPORT_RECORDS=500000
EXPORT_BATCH_SIZE=10000
```

**Para producción con PostgreSQL:**

```env
# Database - PostgreSQL para producción
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/inventory_db

# JWT Security - Generar clave segura
SECRET_KEY=tu-clave-super-secreta-generada-con-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False

# CORS - Solo tus dominios
ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

**Generar SECRET_KEY seguro:**

```bash
# En Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

### Paso 5: Inicializar Base de Datos

```bash
# Ejecutar script de inicialización
python init_db.py
```

**Salida esperada:**

```
============================================================
Inventory API - Database Initialization
============================================================
Creating database tables...
✓ Database tables created successfully!

¿Deseas crear datos de ejemplo? (s/n): s

Creating sample data...
Creating admin user...
✓ Admin user created
Creating sample products...
✓ Sample products created

============================================================
✓ Sample data created successfully!
============================================================

Sample User Credentials:
  Username: admin
  Email: admin@example.com
  Password: admin123
============================================================
```

**Notas:**
- Los datos de ejemplo incluyen 5 productos y 1 usuario admin
- Puedes omitir los datos de ejemplo respondiendo "n"

### Paso 6: Verificar Estructura de Archivos

Tu proyecto debe tener esta estructura:

```
inventory-api/
├── app/                      # Backend
│   ├── __init__.py
│   ├── main.py              # Aplicación principal
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión a BD
│   ├── models/              # Modelos de datos
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── import_log.py
│   ├── schemas/             # Validación (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── import_log.py
│   ├── routers/             # Endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   └── import_export.py
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── product.py
│   │   └── import_export.py
│   └── utils/               # Utilidades
│       ├── __init__.py
│       ├── security.py
│       └── dependencies.py
├── frontend/                 # Frontend
│   ├── index.html           # Página principal
│   ├── css/
│   │   └── styles.css       # Estilos
│   ├── js/
│   │   ├── api.js          # Comunicación API
│   │   └── app.js          # Lógica aplicación
│   ├── README.md
│   └── GUIA_RAPIDA.md
├── examples/                 # Archivos de ejemplo
│   ├── productos_ejemplo.csv
│   └── productos_ejemplo.xlsx
├── tests/                    # Tests
│   ├── __init__.py
│   └── test_api.py
├── .env                      # Variables de entorno (crear)
├── .env.example             # Ejemplo de variables
├── .gitignore
├── requirements.txt         # Dependencias Python
├── init_db.py              # Script inicialización BD
├── fix_bcrypt.py           # Script arreglo bcrypt
├── README.md               # Este archivo
├── TECHNICAL_DOCS.md       # Documentación técnica
├── RESUMEN_EJECUTIVO.md    # Resumen del proyecto
└── Inventory_API_Postman_Collection.json  # Colección Postman
```

---

## 🚀 Ejecutar la Aplicación

### Desarrollo

```bash
# Asegúrate de estar en el directorio del proyecto
cd Prueba_Api_Python

# Asegúrate de que el entorno virtual esté activado
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Iniciar servidor en modo desarrollo (con recarga automática)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**

```
INFO:     Will watch for changes in these directories: ['/path/to/inventory-api']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Producción

```bash
# Con Uvicorn 
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4


```
---

## 🌐 Acceder a la Aplicación

Una vez que el servidor esté corriendo:

### 🎨 Interfaz Web (Frontend)
```
http://localhost:8000
```

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

### 📚 Documentación de la API

**Swagger UI (interactiva):**
```
http://localhost:8000/docs
```

**OpenAPI JSON:**
```
http://localhost:8000/openapi.json
```

---

## 📖 Guía de Uso

### Usando la Interfaz Web 🎨

#### 1. Login / Registro

**Primera vez - Crear cuenta:**
1. Abre http://localhost:8000
2. Click en "Regístrate aquí"
3. Completa el formulario:
   - Usuario (mínimo 3 caracteres)
   - Email válido
   - Contraseña (mínimo 6 caracteres)
4. Click en "Crear Cuenta"
5. Vuelve a la pantalla de login
6. Inicia sesión con tus credenciales

**Usuario existente:**
1. Ingresa usuario y contraseña
2. Click en "Iniciar Sesión"

#### 2. Dashboard

Al entrar verás:

**Estadísticas (4 tarjetas):**
- 📦 **Total Productos**: Cantidad total en inventario
- 📦 **Stock Total**: Suma de todas las unidades
- 🏷️ **Categorías**: Número de categorías diferentes
- 💰 **Valor Total**: Valor total del inventario (precio × stock)

**Productos Recientes:**
- Los últimos 5 productos agregados al sistema

#### 3. Gestión de Productos

**Crear Producto Nuevo:**
1. Click en sidebar: "📦 Productos"
2. Click en botón "+ Nuevo Producto"
3. Completar formulario:
   - **Nombre** (obligatorio): Ej. "Laptop Dell Inspiron 15"
   - **Descripción** (opcional): Detalles del producto
   - **Precio** (obligatorio): Ej. 899.99
   - **Stock** (obligatorio): Ej. 50
   - **Categoría** (obligatorio): Ej. "Electrónica"
4. Click en "Guardar"

**Buscar Productos:**
- En la barra de búsqueda, escribe parte del nombre
- Los resultados se filtran automáticamente
- La búsqueda es insensible a mayúsculas

**Filtrar Productos:**
- **Por categoría**: Selecciona del dropdown
- **Por precio**: Ingresa precio mínimo y/o máximo
- **Combinar filtros**: Usa varios a la vez

**Editar Producto:**
1. Click en el icono de lápiz (✏️) en la tarjeta del producto
2. Modifica los campos que necesites
3. Click en "Guardar"

**Eliminar Producto:**
1. Click en el icono de basura (🗑️)
2. Confirma la eliminación
3. El producto se elimina inmediatamente

#### 4. Importar/Exportar

**Importar Productos desde CSV/Excel:**

1. Prepara tu archivo con estas columnas obligatorias:
   ```
   nombre, descripcion, precio, stock, categoria
   ```

2. Ejemplo de contenido:
   ```csv
   nombre,descripcion,precio,stock,categoria
   Laptop HP,Laptop con 8GB RAM,699.99,100,Electrónica
   Mouse Logitech,Mouse inalámbrico,25.99,500,Accesorios
   ```

3. Ve a "📤 Importar/Exportar"
4. Click en "Seleccionar archivo" o arrastra el archivo
5. Click en "Importar"
6. Revisa el resultado:
   - ✅ Productos importados correctamente
   - ❌ Productos con errores (se muestran detalles)

**Archivos de ejemplo incluidos:**
- `examples/productos_ejemplo.csv`
- `examples/productos_ejemplo.xlsx`

**Exportar Productos:**

1. Ve a "📤 Importar/Exportar"
2. Click en "Exportar CSV" o "Exportar Excel"
3. El archivo se descarga automáticamente
4. Abre con Excel, Google Sheets, etc.

**Ver Historial de Importaciones:**
- En la parte inferior de "Importar/Exportar"
- Muestra:
  - Nombre del archivo
  - Total de registros procesados
  - Registros exitosos vs fallidos
  - Fecha y hora
  - Estado (completado/fallido)

---

### Usando la API (Programático) 💻

#### Autenticación

**1. Registrar Usuario**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "miusuario",
    "email": "usuario@example.com",
    "password": "mipassword123"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "username": "miusuario",
  "email": "usuario@example.com",
  "created_at": "2026-01-08T00:00:00"
}
```

**2. Iniciar Sesión**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=miusuario&password=mipassword123"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Guarda el token** para usarlo en las siguientes peticiones.

#### Gestión de Productos

**Variables de entorno (para los ejemplos):**
```bash
export TOKEN="tu-token-aqui"
export API="http://localhost:8000/api/v1"
```

**1. Listar Productos**

```bash
curl -X GET "$API/products?skip=0&limit=50" \
  -H "Authorization: Bearer $TOKEN"
```

**Con filtros:**
```bash
curl -X GET "$API/products?categoria=Electrónica&precio_min=100&precio_max=1000" \
  -H "Authorization: Bearer $TOKEN"
```

**2. Obtener Producto por ID**

```bash
curl -X GET "$API/products/1" \
  -H "Authorization: Bearer $TOKEN"
```

**3. Crear Producto**

```bash
curl -X POST "$API/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell Inspiron 15",
    "descripcion": "Laptop con Intel Core i7, 16GB RAM, 512GB SSD",
    "precio": 899.99,
    "stock": 50,
    "categoria": "Electrónica"
  }'
```

**4. Actualizar Producto**

```bash
curl -X PUT "$API/products/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 849.99,
    "stock": 45
  }'
```

**5. Eliminar Producto**

```bash
curl -X DELETE "$API/products/1" \
  -H "Authorization: Bearer $TOKEN"
```

#### Importar/Exportar

**1. Importar Productos**

```bash
curl -X POST "$API/products/import" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@productos.csv"
```

**2. Exportar a CSV**

```bash
curl -X GET "$API/products/export/csv" \
  -H "Authorization: Bearer $TOKEN" \
  --output productos_export.csv
```

**3. Exportar a Excel**

```bash
curl -X GET "$API/products/export/excel" \
  -H "Authorization: Bearer $TOKEN" \
  --output productos_export.xlsx
```

**4. Ver Logs de Importación**

```bash
curl -X GET "$API/products/import-logs?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Instalar dependencias de testing (si no están)
pip install pytest pytest-cov pytest-asyncio httpx

# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=app tests/

# Con reporte HTML
pytest --cov=app --cov-report=html tests/

# Ver reporte
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

### Usar Colección de Postman

1. Abre Postman
2. Click en "Import"
3. Selecciona el archivo: `Inventory_API_Postman_Collection.json`
4. La colección se importa con todos los endpoints
5. Configura la variable `{{base_url}}` a `http://localhost:8000`
6. Ejecuta "Login" primero para obtener el token
7. El token se guarda automáticamente en `{{access_token}}`
8. Prueba los demás endpoints

---

## 🔧 Configuración Avanzada

### Base de Datos PostgreSQL

**1. Instalar PostgreSQL:**
- Windows: https://www.postgresql.org/download/windows/
- Linux: `sudo apt-get install postgresql`
- Mac: `brew install postgresql`

**2. Crear base de datos:**

```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE inventory_db;

-- Crear usuario (opcional)
CREATE USER inventory_user WITH PASSWORD 'tu_password';

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;

-- Salir
\q
```

**3. Actualizar `.env`:**

```env
DATABASE_URL=postgresql://inventory_user:tu_password@localhost:5432/inventory_db
```

**4. Reinicializar base de datos:**

```bash
python init_db.py
```

### Configurar CORS

Si tu frontend está en otro dominio:

```env
# En .env
ALLOWED_ORIGINS=http://localhost:3000,https://miapp.com,https://www.miapp.com
```

### Cambiar Puerto

```bash
# Puerto 3000 en lugar de 8000
uvicorn app.main:app --reload --port 3000
```

### Habilitar HTTPS (Producción)

```bash
# Con certificado SSL
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 443 \
  --ssl-keyfile=/path/to/key.pem \
  --ssl-certfile=/path/to/cert.pem
```

### Variables de Entorno Adicionales

```env
# Tamaño máximo de archivo
MAX_UPLOAD_SIZE=20971520  # 20MB

# Carpeta de uploads
UPLOAD_FOLDER=./uploads

# Paginación
DEFAULT_PAGE_SIZE=100
MAX_PAGE_SIZE=5000

# Exportación
MAX_EXPORT_RECORDS=1000000
EXPORT_BATCH_SIZE=50000
```

---

## 📊 Estructura de Datos

### Modelo de Usuario (User)

```python
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "created_at": "2026-01-08T00:00:00",
  "updated_at": "2026-01-08T00:00:00"
}
```

### Modelo de Producto (Product)

```python
{
  "id": 1,
  "nombre": "Laptop Dell Inspiron 15",
  "descripcion": "Laptop con Intel Core i7",
  "precio": 899.99,
  "stock": 50,
  "categoria": "Electrónica",
  "created_at": "2026-01-08T00:00:00",
  "updated_at": "2026-01-08T00:00:00"
}
```

### Modelo de Log de Importación (ImportLog)

```python
{
  "id": 1,
  "filename": "productos.csv",
  "total_rows": 100,
  "successful_rows": 95,
  "failed_rows": 5,
  "errors": "[...]",  # JSON con detalles de errores
  "status": "completed",  # completed, processing, failed
  "started_at": "2026-01-08T00:00:00",
  "completed_at": "2026-01-08T00:05:00"
}
```

---

## 🚨 Solución de Problemas

### Problema: Error al iniciar el servidor

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solución:**
```bash
# Verificar que el entorno virtual esté activado
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Error de base de datos

**Error:** `OperationalError: unable to open database file`

**Solución:**
```bash
# Verificar permisos de escritura en el directorio
chmod 755 .

# Verificar que DATABASE_URL en .env sea correcto
cat .env | grep DATABASE_URL

# Reinicializar base de datos
python init_db.py
```

### Problema: Error de bcrypt

**Error:** `password cannot be longer than 72 bytes`

**Solución:**
```bash
# Ejecutar script de arreglo
python fix_bcrypt.py

# O manualmente:
pip uninstall bcrypt passlib -y
pip install bcrypt==4.0.1 passlib[bcrypt]==1.7.4

# Reinicializar BD
python init_db.py
```

### Problema: CORS error en el frontend

**Error:** `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solución:**

1. Verificar que el frontend esté accediendo desde `http://localhost:8000`
2. Si usas otro puerto/dominio, actualizar `.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000,http://tudominio.com
   ```
3. Reiniciar el servidor

### Problema: No se puede importar archivos

**Error:** Importación falla o muestra errores

**Solución:**

1. Verificar formato del archivo:
   ```csv
   nombre,descripcion,precio,stock,categoria
   Producto1,Descripción,99.99,100,Categoría
   ```

2. Verificar que:
   - Los precios usen punto decimal (99.99, no 99,99)
   - El stock sea número entero
   - No haya campos vacíos en columnas obligatorias

3. Revisar el log de importación para errores específicos

### Problema: Token expirado

**Error:** `401 Unauthorized` o `Could not validate credentials`

**Solución:**
- El token expira después de 30 minutos
- Vuelve a hacer login para obtener un nuevo token
- O aumenta `ACCESS_TOKEN_EXPIRE_MINUTES` en `.env`

### Problema: Frontend no carga

**Error:** Página en blanco o error 404

**Solución:**

1. Verificar que la carpeta `frontend/` existe
2. Verificar que `frontend/index.html` existe
3. Reiniciar el servidor
4. Limpiar caché del navegador (Ctrl+F5)

---

## 📈 Optimización y Rendimiento

### Para Grandes Volúmenes de Datos

**Importación:**
- Usa archivos CSV (más rápidos que Excel)
- El sistema procesa en lotes de 1000 registros
- Puede manejar +100k registros sin problemas

**Exportación:**
- Usa streaming para archivos grandes
- No consume toda la memoria
- Soporta millones de registros

**Base de Datos:**
- Usa PostgreSQL en producción
- Índices automáticos en campos de búsqueda
- Paginación en todos los listados

### Mejorar Velocidad

```bash
# Usar más workers (CPU cores * 2 + 1)
uvicorn app.main:app --workers 4

# O con Gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

---

## 🔒 Seguridad

### Buenas Prácticas Implementadas

✅ **Contraseñas hasheadas** con bcrypt
✅ **Tokens JWT** con expiración
✅ **Validación de datos** con Pydantic
✅ **CORS** configurado
✅ **SQL Injection** protegido por ORM
✅ **Límite de tamaño** de archivos
✅ **Validación de tipos** de archivos

### Para Producción

1. **Cambiar SECRET_KEY:**
   ```bash
   # Generar nueva clave
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Actualizar en .env
   SECRET_KEY=tu-nueva-clave-generada
   ```

2. **Deshabilitar DEBUG:**
   ```env
   DEBUG=False
   ```

3. **Configurar HTTPS:**
   - Usar certificado SSL
   - Forzar HTTPS en producción

4. **Configurar CORS correctamente:**
   ```env
   ALLOWED_ORIGINS=https://tudominio.com
   ```

5. **Usar PostgreSQL:**
   - No usar SQLite en producción

6. **Backups regulares:**
   ```bash
   # PostgreSQL
   pg_dump inventory_db > backup_$(date +%Y%m%d).sql
   ```

---

## 📚 Documentación Adicional

### Archivos de Documentación Incluidos

- **README.md** (este archivo) - Documentación completa
- **TECHNICAL_DOCS.md** - Arquitectura y detalles técnicos
- **RESUMEN_EJECUTIVO.md** - Resumen del proyecto
- **SOLUCION_BCRYPT.md** - Solución a problemas de bcrypt
- **frontend/README.md** - Documentación del frontend
- **frontend/GUIA_RAPIDA.md** - Guía rápida para usuarios

### Endpoints de la API

Consulta la documentación interactiva en:
- http://localhost:8000/docs (Swagger)
- http://localhost:8000/redoc (ReDoc)

### Arquitectura del Sistema

```
┌─────────────┐     HTTP      ┌──────────────┐
│   Frontend  │ ◄────────────► │   FastAPI    │
│   (HTML/JS) │                │   Backend    │
└─────────────┘                └──────┬───────┘
                                      │
                               ┌──────▼───────┐
                               │  SQLAlchemy  │
                               │     ORM      │
                               └──────┬───────┘
                                      │
                               ┌──────▼───────┐
                               │  PostgreSQL  │
                               │   Database   │
                               └──────────────┘
```

---

## 🤝 Contribución

### Reportar Bugs

Si encuentras un bug:
1. Verifica que no esté ya reportado
2. Crea un issue con:
   - Descripción del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Screenshots (si aplica)
   - Información del sistema

### Sugerir Mejoras

Para sugerir nuevas características:
1. Crea un issue con:
   - Descripción de la característica
   - Casos de uso
   - Beneficios esperados

### Pull Requests

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/NuevaCaracteristica`
3. Commit cambios: `git commit -m 'Agrega nueva característica'`
4. Push: `git push origin feature/NuevaCaracteristica`
5. Abre un Pull Request

---

## 📝 Changelog

### Version 1.0.0 (2026-01-08)

**Backend:**
- ✅ API RESTful completa con FastAPI
- ✅ Autenticación JWT
- ✅ CRUD de productos
- ✅ Importación/Exportación CSV/Excel
- ✅ Sistema de auditoría
- ✅ Optimización para +100k registros
- ✅ Documentación automática

**Frontend:**
- ✅ Interfaz web moderna
- ✅ Dashboard con estadísticas
- ✅ Gestión visual de productos
- ✅ Búsqueda y filtros
- ✅ Importación/Exportación con UI
- ✅ Diseño responsive

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

Desarrollado como prueba técnica de Desarrollador Laravel, implementado en Python/FastAPI.

---

## 📞 Soporte

### Recursos de Ayuda

- **Documentación API:** http://localhost:8000/docs
- **Guía de Usuario:** `frontend/GUIA_RAPIDA.md`
- **Documentación Técnica:** `TECHNICAL_DOCS.md`
- **Issues:** Reportar en el repositorio

### Comunidad

- Python: https://docs.python.org/
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

---

## 🎓 Recursos de Aprendizaje

Si quieres aprender más sobre las tecnologías usadas:

### Backend
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Introduction](https://jwt.io/introduction)

### Frontend
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript.info](https://javascript.info/)
- [CSS Tricks](https://css-tricks.com/)

---

## ⭐ Características Futuras

Posibles mejoras para futuras versiones:

- [ ] Sistema de roles y permisos
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Gráficos y reportes avanzados
- [ ] Modo oscuro en frontend
- [ ] Aplicación móvil
- [ ] Integración con sistemas externos
- [ ] API rate limiting
- [ ] Caché con Redis
- [ ] Procesamiento asíncrono con Celery
- [ ] Multiidioma
- [ ] Auditoría completa de cambios
- [ ] Sistema de alertas automáticas

---

## 🎉 Agradecimientos

Gracias por usar Inventory Manager. Si te ha sido útil, ¡compártelo!

**¿Preguntas? ¿Sugerencias?** No dudes en contactar o abrir un issue.

---

**Made with ❤️ using Python & FastAPI**

*Última actualización: Enero 2026*
