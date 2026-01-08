from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List, Dict
import pandas as pd
import io
import json
from datetime import datetime
from app.models.product import Product
from app.models.import_log import ImportLog
from app.schemas.product import ProductCreate
from app.services.product import ProductService
from pydantic import ValidationError


class ImportExportService:
    """Service for import/export operations."""
    
    ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls']
    REQUIRED_COLUMNS = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
    BATCH_SIZE = 1000  # Insert in batches for better performance
    
    @staticmethod
    def validate_file_extension(filename: str) -> str:
        """
        Validate file extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            File extension
            
        Raises:
            HTTPException: If extension is not allowed
        """
        extension = filename.split('.')[-1].lower()
        
        if extension not in ImportExportService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato de archivo no permitido. Use: {', '.join(ImportExportService.ALLOWED_EXTENSIONS)}"
            )
        
        return extension
    
    @staticmethod
    async def read_file_to_dataframe(file: UploadFile) -> pd.DataFrame:
        """
        Read uploaded file and convert to DataFrame.
        
        Args:
            file: Uploaded file
            
        Returns:
            Pandas DataFrame
            
        Raises:
            HTTPException: If file cannot be read
        """
        extension = ImportExportService.validate_file_extension(file.filename)
        
        try:
            content = await file.read()
            
            if extension == 'csv':
                df = pd.read_csv(io.BytesIO(content))
            else:  # xlsx or xls
                df = pd.read_excel(io.BytesIO(content))
            
            return df
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al leer el archivo: {str(e)}"
            )
    
    @staticmethod
    def validate_dataframe_columns(df: pd.DataFrame) -> None:
        """
        Validate that DataFrame has required columns.
        
        Args:
            df: Pandas DataFrame
            
        Raises:
            HTTPException: If required columns are missing
        """
        missing_columns = [col for col in ImportExportService.REQUIRED_COLUMNS if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Columnas requeridas faltantes: {', '.join(missing_columns)}"
            )
    
    @staticmethod
    def validate_row(row_data: dict, row_number: int) -> tuple[bool, str]:
        """
        Validate a single row of data.
        
        Args:
            row_data: Dictionary with row data
            row_number: Row number for error reporting
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Clean NaN values
            for key, value in row_data.items():
                if pd.isna(value):
                    row_data[key] = None if key == 'descripcion' else ''
            
            # Validate using Pydantic schema
            ProductCreate(**row_data)
            return True, ""
        
        except ValidationError as e:
            errors = []
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                message = error['msg']
                errors.append(f"{field}: {message}")
            
            return False, f"Fila {row_number}: {'; '.join(errors)}"
        
        except Exception as e:
            return False, f"Fila {row_number}: Error desconocido - {str(e)}"
    
    @staticmethod
    async def import_products(
        db: Session,
        file: UploadFile
    ) -> Dict:
        """
        Import products from CSV or Excel file.
        
        Args:
            db: Database session
            file: Uploaded file
            
        Returns:
            Dictionary with import results
        """
        # Create import log
        import_log = ImportLog(
            filename=file.filename,
            status="processing"
        )
        db.add(import_log)
        db.commit()
        db.refresh(import_log)
        
        try:
            # Read file
            df = await ImportExportService.read_file_to_dataframe(file)
            ImportExportService.validate_dataframe_columns(df)
            
            total_rows = len(df)
            successful_rows = 0
            failed_rows = 0
            errors = []
            valid_products = []
            
            # Process rows
            for idx, row in df.iterrows():
                row_number = idx + 2  # +2 because Excel rows start at 1 and we have header
                row_data = row.to_dict()
                
                # Validate row
                is_valid, error_message = ImportExportService.validate_row(row_data, row_number)
                
                if is_valid:
                    # Clean data for insertion
                    if pd.isna(row_data.get('descripcion')):
                        row_data['descripcion'] = None
                    
                    valid_products.append(row_data)
                    successful_rows += 1
                    
                    # Insert in batches for performance
                    if len(valid_products) >= ImportExportService.BATCH_SIZE:
                        ProductService.bulk_create_products(db, valid_products)
                        valid_products = []
                else:
                    failed_rows += 1
                    errors.append({
                        "row": row_number,
                        "error": error_message
                    })
            
            # Insert remaining products
            if valid_products:
                ProductService.bulk_create_products(db, valid_products)
            
            # Update import log
            import_log.total_rows = total_rows
            import_log.successful_rows = successful_rows
            import_log.failed_rows = failed_rows
            import_log.errors = json.dumps(errors) if errors else None
            import_log.status = "completed"
            import_log.completed_at = datetime.utcnow()
            
            db.commit()
            
            return {
                "log_id": import_log.id,
                "filename": file.filename,
                "total_rows": total_rows,
                "successful_rows": successful_rows,
                "failed_rows": failed_rows,
                "status": "completed",
                "message": f"Importación completada: {successful_rows} exitosos, {failed_rows} fallidos",
                "errors": errors[:100] if errors else None  # Limit errors in response
            }
        
        except Exception as e:
            # Update import log with error
            import_log.status = "failed"
            import_log.errors = json.dumps([{"error": str(e)}])
            import_log.completed_at = datetime.utcnow()
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error durante la importación: {str(e)}"
            )
    
    @staticmethod
    def export_to_csv(db: Session) -> bytes:
        """
        Export all products to CSV.
        
        Args:
            db: Database session
            
        Returns:
            CSV file content as bytes
        """
        products = ProductService.get_all_products_for_export(db)
        
        # Convert to list of dictionaries
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'nombre': product.nombre,
                'descripcion': product.descripcion,
                'precio': product.precio,
                'stock': product.stock,
                'categoria': product.categoria
            })
        
        # Create DataFrame and convert to CSV
        df = pd.DataFrame(data)
        
        # Use StringIO to get CSV as string
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_content = output.getvalue()
        
        return csv_content.encode('utf-8')
    
    @staticmethod
    def export_to_excel(db: Session) -> bytes:
        """
        Export all products to Excel.
        
        Args:
            db: Database session
            
        Returns:
            Excel file content as bytes
        """
        products = ProductService.get_all_products_for_export(db)
        
        # Convert to list of dictionaries
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'nombre': product.nombre,
                'descripcion': product.descripcion,
                'precio': product.precio,
                'stock': product.stock,
                'categoria': product.categoria
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Use BytesIO to get Excel as bytes
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Productos')
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def get_import_logs(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[ImportLog], int]:
        """
        Get import logs with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of import logs, total count)
        """
        query = db.query(ImportLog).order_by(ImportLog.started_at.desc())
        total = query.count()
        logs = query.offset(skip).limit(limit).all()
        
        return logs, total
