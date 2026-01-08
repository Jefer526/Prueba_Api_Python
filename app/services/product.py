from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Service for product-related operations."""
    
    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        categoria: Optional[str] = None,
        nombre: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        stock_min: Optional[int] = None
    ) -> tuple[List[Product], int]:
        """
        Get a list of products with optional filters.
        
        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            categoria: Filter by category
            nombre: Filter by name (partial match)
            precio_min: Filter by minimum price
            precio_max: Filter by maximum price
            stock_min: Filter by minimum stock
            
        Returns:
            Tuple of (list of products, total count)
        """
        query = db.query(Product)
        
        # Apply filters
        filters = []
        if categoria:
            filters.append(Product.categoria == categoria)
        if nombre:
            filters.append(Product.nombre.ilike(f"%{nombre}%"))
        if precio_min is not None:
            filters.append(Product.precio >= precio_min)
        if precio_max is not None:
            filters.append(Product.precio <= precio_max)
        if stock_min is not None:
            filters.append(Product.stock >= stock_min)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        """
        Get a single product by ID.
        
        Args:
            db: Database session
            product_id: Product ID
            
        Returns:
            Product object
            
        Raises:
            HTTPException: If product not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        return product
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """
        Create a new product.
        
        Args:
            db: Database session
            product_data: Product creation data
            
        Returns:
            The created Product object
        """
        db_product = Product(**product_data.model_dump())
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        return db_product
    
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate
    ) -> Product:
        """
        Update an existing product.
        
        Args:
            db: Database session
            product_id: Product ID
            product_data: Product update data
            
        Returns:
            The updated Product object
            
        Raises:
            HTTPException: If product not found
        """
        product = ProductService.get_product(db, product_id)
        
        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> dict:
        """
        Delete a product.
        
        Args:
            db: Database session
            product_id: Product ID
            
        Returns:
            Dictionary with success message
            
        Raises:
            HTTPException: If product not found
        """
        product = ProductService.get_product(db, product_id)
        
        db.delete(product)
        db.commit()
        
        return {"message": f"Producto '{product.nombre}' eliminado exitosamente"}
    
    @staticmethod
    def get_all_products_for_export(db: Session) -> List[Product]:
        """
        Get all products for export (no pagination).
        
        Args:
            db: Database session
            
        Returns:
            List of all products
        """
        return db.query(Product).all()
    
    @staticmethod
    def bulk_create_products(db: Session, products_data: List[dict]) -> int:
        """
        Bulk create multiple products.
        
        Args:
            db: Database session
            products_data: List of product dictionaries
            
        Returns:
            Number of products created
        """
        products = [Product(**data) for data in products_data]
        db.bulk_save_objects(products)
        db.commit()
        
        return len(products)
