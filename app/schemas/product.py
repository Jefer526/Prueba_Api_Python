from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


class ProductBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    stock: int = Field(..., ge=0, description="Stock disponible (no puede ser negativo)")
    categoria: str = Field(..., min_length=1, max_length=100, description="Categoría del producto")
    
    @validator('precio')
    def validate_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2)
    
    @validator('stock')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=255)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    
    @validator('precio')
    def validate_precio(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2) if v is not None else v
    
    @validator('stock')
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ProductResponse]


class ProductFilter(BaseModel):
    categoria: Optional[str] = None
    nombre: Optional[str] = None
    precio_min: Optional[float] = None
    precio_max: Optional[float] = None
    stock_min: Optional[int] = None
