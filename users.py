from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import User
from ..security import verify_password, create_token

router = APIRouter(prefix='/auth', tags=['auth'])

class LoginIn(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(data: LoginIn):
    try:
        user = User.get(User.username == data.username)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'sub': user.username, 'role': user.role, 'uid': user.id})
    return {'access_token': token, 'token_type': 'bearer', 'role': user.role, 'username': user.username}
