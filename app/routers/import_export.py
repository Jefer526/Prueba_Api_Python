from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.import_log import ImportResult, ImportLogListResponse
from app.services.import_export import ImportExportService
from app.utils.dependencies import get_current_active_user
from app.config import settings
import io

router = APIRouter(
    prefix="/products",
    tags=["Importación/Exportación"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/import", response_model=ImportResult)
async def import_products(
    file: UploadFile = File(..., description="Archivo CSV o Excel con productos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Importar productos desde un archivo CSV o Excel.
    
    **Formato del archivo:**
    
    El archivo debe contener las siguientes columnas:
    - nombre: Nombre del producto (obligatorio, mínimo 3 caracteres)
    - descripcion: Descripción del producto (opcional)
    - precio: Precio del producto (obligatorio, numérico, mayor a 0)
    - stock: Cantidad en stock (obligatorio, numérico, no negativo)
    - categoria: Categoría del producto (obligatorio)
    
    **Ejemplo CSV:**
    ```
    nombre,descripcion,precio,stock,categoria
    Laptop Dell,Laptop Dell Inspiron 15,899.99,50,Electrónica
    Mouse Logitech,Mouse inalámbrico,25.99,200,Accesorios
    ```
    
    **Validaciones:**
    - Todos los registros son validados antes de insertarse
    - Los errores de validación se registran en la tabla de auditoría
    - Se procesan lotes de 1000 registros para optimizar el rendimiento
    
    **Respuesta:**
    - Retorna un resumen con el número de registros exitosos y fallidos
    - Los primeros 100 errores se incluyen en la respuesta
    - Todos los errores se guardan en el log de importación
    """
    return await ImportExportService.import_products(db, file)


@router.get("/export/csv")
async def export_products_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Exportar todos los productos a formato CSV.
    
    Descarga un archivo CSV con todos los productos del inventario.
    El archivo incluye las columnas: id, nombre, descripcion, precio, stock, categoria.
    
    **Optimización:**
    - Soporta grandes volúmenes de datos (+100k registros)
    - Utiliza streaming para evitar consumo excesivo de memoria
    """
    csv_content = ImportExportService.export_to_csv(db)
    
    return StreamingResponse(
        io.BytesIO(csv_content),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=productos_export.csv"
        }
    )


@router.get("/export/excel")
async def export_products_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Exportar todos los productos a formato Excel.
    
    Descarga un archivo Excel (.xlsx) con todos los productos del inventario.
    El archivo incluye las columnas: id, nombre, descripcion, precio, stock, categoria.
    
    **Optimización:**
    - Soporta grandes volúmenes de datos (+100k registros)
    - Utiliza streaming para evitar consumo excesivo de memoria
    """
    excel_content = ImportExportService.export_to_excel(db)
    
    return StreamingResponse(
        io.BytesIO(excel_content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=productos_export.xlsx"
        }
    )


@router.get("/import-logs", response_model=ImportLogListResponse)
async def get_import_logs(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Número máximo de registros a retornar"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener el historial de importaciones.
    
    Retorna una lista paginada de todos los logs de importación,
    incluyendo el estado, número de registros procesados y errores.
    
    Los logs están ordenados del más reciente al más antiguo.
    """
    logs, total = ImportExportService.get_import_logs(db, skip, limit)
    
    return ImportLogListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=logs
    )
