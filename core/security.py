from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, password_hash: str) -> bool:
    return CRIPTO.verify(password, password_hash)

def generate_hash(password: str) -> str:
    return CRIPTO.hash(password)