from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.services.product import ProductService
from app.utils.dependencies import get_current_active_user
from app.config import settings

router = APIRouter(
    prefix="/products",
    tags=["Productos"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("", response_model=ProductListResponse)
async def get_products(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Número máximo de registros a retornar"
    ),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    nombre: Optional[str] = Query(None, description="Buscar por nombre (parcial)"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    stock_min: Optional[int] = Query(None, ge=0, description="Stock mínimo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de productos con filtros opcionales y paginación.
    
    **Filtros disponibles:**
    - categoria: Filtrar por categoría exacta
    - nombre: Buscar productos que contengan el texto (insensible a mayúsculas)
    - precio_min: Productos con precio mayor o igual al especificado
    - precio_max: Productos con precio menor o igual al especificado
    - stock_min: Productos con stock mayor o igual al especificado
    
    **Paginación:**
    - skip: Número de registros a omitir (default: 0)
    - limit: Número máximo de registros a retornar (default: 50, máx: 1000)
    """
    products, total = ProductService.get_products(
        db=db,
        skip=skip,
        limit=limit,
        categoria=categoria,
        nombre=nombre,
        precio_min=precio_min,
        precio_max=precio_max,
        stock_min=stock_min
    )
    
    return ProductListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=products
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un producto específico por ID.
    """
    return ProductService.get_product(db, product_id)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear un nuevo producto.
    
    **Campos requeridos:**
    - nombre: Nombre del producto (3-255 caracteres)
    - precio: Precio del producto (debe ser mayor a 0)
    - stock: Cantidad en stock (no puede ser negativo)
    - categoria: Categoría del producto
    
    **Campos opcionales:**
    - descripcion: Descripción del producto
    """
    return ProductService.create_product(db, product_data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar un producto existente.
    
    Solo se actualizarán los campos proporcionados en la petición.
    Los campos omitidos mantendrán sus valores actuales.
    """
    return ProductService.update_product(db, product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar un producto.
    """
    return ProductService.delete_product(db, product_id)
