from passlib.context import CryptContext
from jose import jwt
from datetime  import datetime, timedelta


SECRET_KEY = "m@ny@tt@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

#This logic is for password hashing

pwd_context = CryptContext(schemes=["bcrypt"], depricated = "auto")

def hash_password(password: str):
    # Hashes plain text password using bcrypt  
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #verifies if hashed password against the password input
    return pwd_context.verify(plain_password, hashed_password)

#This logic is for jwt using jose

def create_access_token(data: dict, expire_time: timedelta | None = None):
    data_cpy = data.copy()

    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_cpy.update({"exp": expire})

    token = jwt.encode(data_cpy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
