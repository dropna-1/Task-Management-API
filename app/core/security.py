from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
password_hash = PasswordHash.recommended()