# 🚀 Guía Rápida - Frontend de Inventory Manager

## ⚡ Inicio en 3 Pasos

### 1. Inicia el Servidor

```bash
uvicorn app.main:app --reload
```

### 2. Abre tu Navegador

```
http://localhost:8000
```

### 3. Inicia Sesión

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 🎨 Tour Rápido de la Interfaz

### Pantalla de Login

![Login](https://via.placeholder.com/800x400/667eea/ffffff?text=Pantalla+de+Login)

- **Iniciar Sesión**: Si ya tienes cuenta
- **Registrarse**: Para crear una cuenta nueva

---

### Dashboard 📊

![Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard)

**Verás 4 tarjetas con estadísticas:**

1. **Total Productos** - Número total de productos en tu inventario
2. **Stock Total** - Suma de todas las unidades
3. **Categorías** - Número de categorías diferentes
4. **Valor Total** - Valor total de tu inventario

**Productos Recientes:**
- Los últimos 5 productos agregados

---

### Gestión de Productos 📦

![Productos](https://via.placeholder.com/800x400/667eea/ffffff?text=Lista+de+Productos)

#### Buscar y Filtrar

- **Barra de búsqueda**: Escribe el nombre del producto
- **Filtro por categoría**: Desplegable con todas las categorías
- **Filtro por precio**: Mínimo y máximo
- **Resultados**: Se actualizan automáticamente

#### Crear Producto Nuevo

1. Click en botón **"+ Nuevo Producto"**
2. Completa el formulario:
   - **Nombre** (obligatorio)
   - **Descripción** (opcional)
   - **Precio** (obligatorio, número decimal)
   - **Stock** (obligatorio, número entero)
   - **Categoría** (obligatorio)
3. Click en **"Guardar"**

#### Editar Producto

1. Click en el icono de **lápiz** (📝) en la tarjeta del producto
2. Modifica los campos que desees
3. Click en **"Guardar"**

#### Eliminar Producto

1. Click en el icono de **basura** (🗑️) en la tarjeta del producto
2. Confirma la eliminación

---

### Importar/Exportar 📤

![Import/Export](https://via.placeholder.com/800x400/667eea/ffffff?text=Importar+y+Exportar)

#### Importar Productos

**Pasos:**

1. Ve a la sección **"Importar/Exportar"**
2. Click en **"Seleccionar archivo"**
3. Elige tu archivo CSV o Excel
4. Click en **"Importar"**
5. Revisa el resultado:
   - ✅ Productos importados exitosamente
   - ❌ Productos con errores

**Formato del archivo:**

```csv
nombre,descripcion,precio,stock,categoria
Laptop Dell,Laptop potente,899.99,50,Electrónica
Mouse Logitech,Mouse inalámbrico,25.99,200,Accesorios
```

**Descarga el archivo de ejemplo:** `examples/productos_ejemplo.csv`

#### Exportar Productos

**Pasos:**

1. Click en **"Exportar CSV"** o **"Exportar Excel"**
2. El archivo se descargará automáticamente
3. Abre el archivo en Excel, Google Sheets, etc.

#### Historial de Importaciones

En la parte inferior verás un registro de todas las importaciones:
- Nombre del archivo
- Total de registros
- Exitosos vs Fallidos
- Fecha y hora
- Estado (completado/fallido)

---

## 🎯 Tips y Trucos

### Búsqueda Rápida

- **Texto parcial**: Escribe solo parte del nombre
- **Insensible a mayúsculas**: "laptop" encuentra "Laptop Dell"
- **Búsqueda instantánea**: Los resultados aparecen mientras escribes

### Filtros Combinados

Puedes usar múltiples filtros a la vez:

```
Categoría: Electrónica
Precio mín: 100
Precio máx: 1000
Buscar: laptop
```

### Navegación Rápida

**Teclado:**
- `Enter` en la búsqueda: Actualiza resultados
- `Esc` en modal: Cierra el formulario
- `Tab`: Navega entre campos del formulario

**Sidebar:**
- 🏠 Dashboard: Vista general
- 📦 Productos: Gestión completa
- 📤 Importar/Exportar: Carga masiva

---

## 💡 Casos de Uso Comunes

### Caso 1: Agregar productos de forma masiva

1. Crea un archivo Excel con tus productos
2. Guárdalo como CSV
3. Ve a "Importar/Exportar"
4. Importa el archivo
5. ¡Listo! Todos tus productos están en el sistema

### Caso 2: Actualizar precios

1. Exporta todos los productos a Excel
2. Modifica los precios en Excel
3. Guarda y cierra Excel
4. Importa el archivo actualizado
5. Los precios se actualizarán automáticamente

### Caso 3: Monitorear stock bajo

1. Ve a "Productos"
2. Los productos con stock < 10 se muestran en rojo
3. Edita y aumenta el stock según necesites

### Caso 4: Generar reporte

1. Filtra los productos que necesitas
2. Exporta a Excel
3. Abre en Excel y genera tu reporte personalizado

---

## 🔒 Seguridad

### Sesión

- Tu sesión expira después de 30 minutos de inactividad
- Puedes cerrar sesión en cualquier momento con el botón **"Salir"**
- Los tokens se guardan de forma segura

### Datos

- Todos los datos se transmiten de forma segura
- Las contraseñas están encriptadas
- Cada usuario solo ve sus propios datos

---

## 🐛 Solución de Problemas

### No puedo iniciar sesión

**Problema**: "Credenciales incorrectas"

**Solución:**
1. Verifica tu usuario y contraseña
2. Si olvidaste tu contraseña, contacta al administrador
3. Puedes crear una cuenta nueva con "Regístrate"

### La importación falla

**Problema**: "Error al importar archivo"

**Solución:**
1. Verifica que el archivo tenga las columnas correctas:
   - nombre, descripcion, precio, stock, categoria
2. Asegúrate de que:
   - Los precios son números (usa punto decimal: 99.99)
   - El stock es un número entero (50, no 50.5)
   - Ningún campo obligatorio está vacío
3. Revisa el historial de importaciones para ver los errores específicos

### Los productos no se cargan

**Problema**: Pantalla en blanco o error

**Solución:**
1. Presiona `F5` para recargar la página
2. Verifica tu conexión a internet
3. Asegúrate de que el backend esté corriendo
4. Revisa la consola del navegador (F12) para ver errores

### El archivo no se exporta

**Problema**: No se descarga el archivo

**Solución:**
1. Verifica los permisos de descarga del navegador
2. Revisa la carpeta de descargas
3. Intenta con otro formato (CSV en lugar de Excel)

---

## 📱 Uso en Móvil

El frontend es completamente responsive:

- ✅ iPhone/Android: Funciona perfectamente
- ✅ Tablet: Vista optimizada
- ✅ Desktop: Experiencia completa

**Nota**: En móvil, el sidebar se oculta automáticamente para más espacio.

---

## 🎨 Personalización

### Cambiar Colores

Edita `frontend/css/styles.css`:

```css
:root {
    --primary: #4f46e5;  /* Tu color principal */
}
```

### Cambiar Logo

En `frontend/index.html`, busca:

```html
<i class="fas fa-boxes"></i>
```

Y cámbialo por el icono que prefieras de [Font Awesome](https://fontawesome.com/icons).

---

## 🚀 Siguiente Nivel

### Agregar más funcionalidades

El código está organizado para fácil extensión:

- `js/app.js`: Lógica de la aplicación
- `js/api.js`: Comunicación con el backend
- `css/styles.css`: Estilos y diseño

### Integrar con otros sistemas

La API es estándar REST, puedes integrarla con:
- Aplicaciones móviles
- Sistemas ERP
- Dashboards personalizados
- Scripts automatizados

---

## ❓ Preguntas Frecuentes

**Q: ¿Puedo tener múltiples usuarios?**  
A: Sí, cada persona puede crear su propia cuenta.

**Q: ¿Los datos se guardan automáticamente?**  
A: Sí, todos los cambios se guardan inmediatamente en la base de datos.

**Q: ¿Puedo usar esto en mi empresa?**  
A: ¡Por supuesto! El sistema está diseñado para uso profesional.

**Q: ¿Necesito internet?**  
A: Solo para acceder al servidor. Si usas localhost, funciona offline.

**Q: ¿Cuántos productos puedo tener?**  
A: El sistema soporta cientos de miles de productos sin problemas.

---

**¡Disfruta gestionando tu inventario!** 🎉

¿Necesitas ayuda? Revisa la documentación completa en `/docs`
