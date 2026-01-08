"""
Database initialization script.

This script creates all database tables and optionally adds sample data.
"""
from app.database import Base, engine
from app.models import User, Product, ImportLog
from sqlalchemy.orm import Session
import sys


def init_db():
    """Initialize database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


def create_sample_data():
    """Create sample data for testing."""
    print("\nCreating sample data...")
    
    db = Session(bind=engine)
    
    try:
        # Check if data already exists
        existing_user = db.query(User).first()
        if existing_user:
            print("Sample data already exists. Skipping...")
            return
        
        # Import password hashing function
        from app.utils.security import get_password_hash
        
        # Create sample user with a simple password
        print("Creating admin user...")
        sample_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(sample_user)
        db.flush()  # Flush to catch any errors before adding products
        print("✓ Admin user created")
        
        # Create sample products
        print("Creating sample products...")
        sample_products = [
            Product(
                nombre="Laptop Dell Inspiron 15",
                descripcion="Laptop Dell con procesador Intel Core i7, 16GB RAM, 512GB SSD",
                precio=899.99,
                stock=50,
                categoria="Electrónica"
            ),
            Product(
                nombre="Mouse Logitech MX Master 3",
                descripcion="Mouse inalámbrico ergonómico",
                precio=99.99,
                stock=200,
                categoria="Accesorios"
            ),
            Product(
                nombre="Teclado Mecánico Keychron K2",
                descripcion="Teclado mecánico inalámbrico con switches Gateron",
                precio=79.99,
                stock=150,
                categoria="Accesorios"
            ),
            Product(
                nombre="Monitor LG UltraWide 34\"",
                descripcion="Monitor curvo 34 pulgadas, resolución 3440x1440",
                precio=449.99,
                stock=30,
                categoria="Electrónica"
            ),
            Product(
                nombre="Silla Ergonómica Herman Miller",
                descripcion="Silla de oficina ergonómica premium",
                precio=1299.99,
                stock=20,
                categoria="Mobiliario"
            )
        ]
        
        for product in sample_products:
            db.add(product)
        
        print("✓ Sample products created")
        
        # Commit all changes
        db.commit()
        
        print("\n" + "=" * 60)
        print("✓ Sample data created successfully!")
        print("=" * 60)
        print("\nSample User Credentials:")
        print("  Username: admin")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error creating sample data: {e}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        print("\n⚠️  Note: Tables were created successfully.")
        print("You can create users through the API using /api/v1/auth/register")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Inventory API - Database Initialization")
    print("=" * 60)
    
    try:
        init_db()
        
        # Ask if user wants to create sample data
        print("\n¿Deseas crear datos de ejemplo? (s/n): ", end='')
        response = input().lower()
        
        if response in ['s', 'si', 'y', 'yes']:
            create_sample_data()
        else:
            print("\nSaltando datos de ejemplo.")
            print("Puedes crear usuarios usando el endpoint /api/v1/auth/register")
    
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Database initialization completed!")
    print("=" * 60)
    print("\nYou can now run the application with:")
    print("  uvicorn app.main:app --reload")
    print("\nAPI Documentation:")
    print("  http://localhost:8000/docs")