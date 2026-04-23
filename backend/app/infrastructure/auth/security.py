from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.infrastructure.settings.config import get_settings

# Usamos PBKDF2-SHA256 para evitar dependencias nativas (ej. bcrypt) que
# suelen romper en versiones nuevas de Python por binarios incompatibles.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
settings = get_settings()


def hash_password(password: str) -> str:
    # Nunca almacenamos contraseñas en texto plano.
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    # Compara password plano vs hash almacenado.
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, role: str) -> str:
    # Genera JWT con subject (id de usuario), rol y expiración.
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    # Decodifica y valida firma/expiración del JWT.
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
