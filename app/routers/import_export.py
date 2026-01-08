from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.import_log import ImportResult
from app.services.import_export import ImportExportService
from app.utils.dependencies import get_current_active_user
import io
from app.models.import_log import ImportLog

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
    """Importar productos desde un archivo CSV o Excel."""
    return await ImportExportService.import_products(db, file)


@router.get("/export/csv")
async def export_products_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Exportar todos los productos a formato CSV."""
    csv_content = ImportExportService.export_to_csv(db)
    
    return StreamingResponse(
        io.BytesIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=productos_export.csv"}
    )


@router.get("/export/excel")
async def export_products_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Exportar todos los productos a formato Excel."""
    excel_content = ImportExportService.export_to_excel(db)
    
    return StreamingResponse(
        io.BytesIO(excel_content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=productos_export.xlsx"}
    )


# Nuevo router separado para import-logs sin el prefix /products
logs_router = APIRouter(
    tags=["Importación/Exportación"],
    dependencies=[Depends(get_current_active_user)]
)


@logs_router.get("/import-logs")
async def get_import_logs(
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener el historial de importaciones."""
    logs, total = ImportExportService.get_import_logs(db, skip, limit)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [
            {
                "id": log.id,
                "filename": log.filename,
                "total_rows": log.total_rows,
                "successful_rows": log.successful_rows,
                "failed_rows": log.failed_rows,
                "errors": log.errors,
                "status": log.status,
                "started_at": str(log.started_at) if log.started_at else None,
                "completed_at": str(log.completed_at) if log.completed_at else None
            }
            for log in logs
        ]
    }

@router.get("/import-logs/{log_id}/download-errors")
async def download_import_errors(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Descargar los registros fallidos de una importación específica en formato CSV.
    """
    # Obtener el log
    import_log = db.query(ImportLog).filter(ImportLog.id == log_id).first()
    
    if not import_log:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log de importación no encontrado"
        )
    
    if not import_log.errors or import_log.failed_rows == 0:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay errores registrados en esta importación"
        )
    
    # Parsear errores
    import json
    try:
        errors = json.loads(import_log.errors)
    except:
        errors = []
    
    # Crear CSV con los errores
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Fila', 'Campo', 'Valor', 'Error'])
    
    # Datos
    for error in errors:
        writer.writerow([
            error.get('row', 'N/A'),
            error.get('field', 'N/A'),
            error.get('value', 'N/A'),
            error.get('error', 'N/A')
        ])
    
    # Convertir a bytes
    csv_content = output.getvalue().encode('utf-8')
    
    return StreamingResponse(
        io.BytesIO(csv_content),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=errores_importacion_{log_id}.csv"
        }
    )