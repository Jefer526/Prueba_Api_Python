from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.config import settings
from app.routers import auth, products, import_export

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    API RESTful para la gestión de productos de un inventario.
    
    ## Características
    
    * **Autenticación JWT** - Sistema de autenticación seguro basado en tokens
    * **CRUD Completo** - Operaciones completas de creación, lectura, actualización y eliminación
    * **Importación Masiva** - Importar productos desde CSV/Excel con validación
    * **Exportación** - Exportar productos a CSV o Excel
    * **Filtros Avanzados** - Búsqueda y filtrado de productos
    * **Auditoría** - Sistema de logs para importaciones
    * **Optimización** - Soporte para grandes volúmenes de datos (+100k registros)
    
    ## Autenticación
    
    La mayoría de los endpoints requieren autenticación. Primero debes:
    
    1. Registrarte usando `/api/v1/auth/register`
    2. Iniciar sesión usando `/api/v1/auth/login` para obtener un token
    3. Usar el token en el header: `Authorization: Bearer <token>`
    
    ## Versionado
    
    Esta API usa versionado de URL. La versión actual es v1.
    Todos los endpoints están bajo el prefijo `/api/v1/`.
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API versioning
API_V1_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(products.router, prefix=API_V1_PREFIX)
app.include_router(import_export.router, prefix=API_V1_PREFIX)
app.include_router(import_export.logs_router, prefix=API_V1_PREFIX)  


# Serve frontend static files - DEBE IR DESPUÉS de los routers
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    # Servir archivos estáticos SIN html=True para no interferir con /redoc y /docs
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """Serve the frontend application."""
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend not found. Please check the frontend directory."}
        
else:
    @app.get("/", tags=["Root"])
    async def root():
        """
        Endpoint raíz de la API.
        
        Retorna información básica sobre la API.
        """
        return {
            "message": "Bienvenido a Inventory API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
            "note": "Frontend not found. Install frontend files in the 'frontend' directory to access the web interface."
        }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verificación de salud de la API.
    
    Útil para monitoreo y balanceadores de carga.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )