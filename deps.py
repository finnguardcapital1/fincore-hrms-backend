from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import verify_token

auth_scheme = HTTPBearer(auto_error=True)

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    data = verify_token(token.credentials)
    return data  # { 'sub': username, 'role': 'admin'|'fgcuser', 'uid': id }

def admin_required(user=Depends(get_current_user)):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin only')
    return user

def fgcuser_allowed(user=Depends(get_current_user)):
    return user
