# 🎨 Frontend - Inventory Manager

Interfaz web moderna y responsive para la API de gestión de inventario.

## 🚀 Características

- ✅ **Autenticación** - Login y registro de usuarios
- 📊 **Dashboard** - Estadísticas en tiempo real
- 📦 **Gestión de Productos** - CRUD completo con interfaz intuitiva
- 🔍 **Búsqueda y Filtros** - Encuentra productos fácilmente
- 📤 **Importar/Exportar** - Carga masiva y descarga de productos
- 📱 **Responsive** - Funciona en móviles, tablets y escritorio
- 🎨 **Diseño Moderno** - UI atractiva con animaciones suaves

## 📁 Estructura

```
frontend/
├── index.html          # Página principal
├── css/
│   └── styles.css      # Estilos completos
└── js/
    ├── api.js          # Comunicación con la API
    └── app.js          # Lógica de la aplicación
```

## 🔧 Configuración

### Opción 1: Servir desde FastAPI (Recomendado)

El backend ya está configurado para servir el frontend automáticamente.

1. Asegúrate de que el frontend esté en la carpeta `frontend/`
2. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Accede a: **http://localhost:8000**

### Opción 2: Servidor Local Simple

Si prefieres usar un servidor independiente:

```bash
# Con Python
cd frontend
python -m http.server 8080

# O con Node.js
npx http-server -p 8080
```

Luego accede a: **http://localhost:8080**

## ⚙️ Configuración de API

La URL de la API se configura en `js/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

Si tu API está en otro puerto o dominio, cámbialo aquí.

## 🎯 Uso

### 1. Iniciar Sesión

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

O crea una cuenta nueva usando el botón "Regístrate".

### 2. Dashboard

- **Vista general** de tu inventario
- **Estadísticas** en tiempo real
- **Productos recientes**

### 3. Gestión de Productos

- **Crear**: Click en "+ Nuevo Producto"
- **Editar**: Click en el icono de editar (lápiz)
- **Eliminar**: Click en el icono de eliminar (basura)
- **Buscar**: Usa la barra de búsqueda
- **Filtrar**: Por categoría, precio, etc.

### 4. Importar/Exportar

**Importar:**
1. Ve a la sección "Importar/Exportar"
2. Selecciona un archivo CSV o Excel
3. Click en "Importar"
4. Revisa el resultado

**Exportar:**
1. Click en "Exportar CSV" o "Exportar Excel"
2. El archivo se descargará automáticamente

## 🎨 Personalización

### Colores

Edita las variables en `css/styles.css`:

```css
:root {
    --primary: #4f46e5;      /* Color principal */
    --secondary: #64748b;    /* Color secundario */
    --success: #10b981;      /* Verde */
    --danger: #ef4444;       /* Rojo */
    /* ... más colores ... */
}
```

### Logo y Branding

1. Cambia el icono en el header (`.auth-header i` y `.sidebar-header i`)
2. Actualiza el nombre en `<h1>Inventory Manager</h1>`

## 📱 Responsive Design

El frontend es completamente responsive:

- **Desktop**: Vista completa con sidebar
- **Tablet**: Diseño adaptado
- **Móvil**: Optimizado para pantallas pequeñas

## 🔒 Seguridad

- Los tokens JWT se guardan en `localStorage`
- Todas las peticiones incluyen autenticación
- Los tokens expiran según configuración del backend
- Logout limpia toda la información local

## 🐛 Troubleshooting

### La API no responde

1. Verifica que el backend esté corriendo: `uvicorn app.main:app --reload`
2. Revisa la URL en `js/api.js`
3. Verifica CORS en el backend (`.env` → `ALLOWED_ORIGINS`)

### Error de CORS

Asegúrate de que en el archivo `.env` del backend tengas:

```env
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:8080,http://localhost:3000
```

### No puedo iniciar sesión

1. Verifica que el usuario existe en la base de datos
2. Revisa la consola del navegador (F12) para ver errores
3. Verifica que el backend esté funcionando correctamente

## 💡 Características Técnicas

- **Sin frameworks**: JavaScript vanilla puro
- **Sin build tools**: No requiere npm, webpack, etc.
- **Font Awesome**: Para iconos modernos
- **Fetch API**: Para comunicación con el backend
- **LocalStorage**: Para persistencia del token
- **CSS Grid/Flexbox**: Para layouts modernos

## 📊 Próximas Mejoras

Posibles extensiones:

- [ ] Gráficos y estadísticas avanzadas
- [ ] Sistema de notificaciones en tiempo real
- [ ] Modo oscuro
- [ ] Exportación personalizada con filtros
- [ ] Gestión de usuarios y permisos
- [ ] Historial de cambios en productos
- [ ] Alertas de stock bajo
- [ ] Dashboard analítico

## 🙋‍♂️ Soporte

Si encuentras algún problema:

1. Revisa la consola del navegador (F12 → Console)
2. Revisa la consola del backend
3. Verifica la configuración de la API

---

**¡Disfruta gestionando tu inventario!** 🎉
