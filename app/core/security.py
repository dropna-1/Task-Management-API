from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")
password_hash = PasswordHash.recommended()