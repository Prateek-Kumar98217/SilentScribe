from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__min_rounds=4,
    bcrypt__max_rounds=16,)

def hash_password(password: str)->str:
    """
    Hash the password
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password: str)-> bool:
    """
    Verify the password
    """
    return pwd_context.verify(plain_password, hashed_password)