"""
Example test file for the Inventory API.

To run tests:
    pytest
    pytest --cov=app tests/
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Setup test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(setup_database):
    """Create a test user."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    return response.json()


@pytest.fixture
def auth_token(test_user):
    """Get authentication token."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    return response.json()["access_token"]


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(setup_database):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"


def test_login(test_user):
    """Test user login."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_product(auth_token):
    """Test product creation."""
    response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "nombre": "Test Product",
            "descripcion": "Test Description",
            "precio": 99.99,
            "stock": 100,
            "categoria": "Test"
        }
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "Test Product"


def test_get_products(auth_token):
    """Test getting products list."""
    response = client.get(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()


def test_unauthorized_access():
    """Test unauthorized access."""
    response = client.get("/api/v1/products")
    assert response.status_code == 401
