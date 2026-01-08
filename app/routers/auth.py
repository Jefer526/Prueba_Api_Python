from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario.
    
    - **username**: Nombre de usuario (3-50 caracteres)
    - **email**: Correo electrónico válido
    - **password**: Contraseña (mínimo 6 caracteres)
    """
    return AuthService.register_user(db, user_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión y obtener token de acceso.
    
    - **username**: Nombre de usuario
    - **password**: Contraseña
    
    Retorna un token JWT que debe ser usado en el header Authorization: Bearer <token>
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    return AuthService.create_token(user)


@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con JSON y obtener token de acceso.
    
    Alternativa al endpoint /login para clientes que prefieren enviar JSON.
    
    - **username**: Nombre de usuario
    - **password**: Contraseña
    """
    user = AuthService.authenticate_user(db, login_data.username, login_data.password)
    return AuthService.create_token(user)
