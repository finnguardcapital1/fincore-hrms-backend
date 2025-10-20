from fastapi import APIRouter, Depends
from ..deps import admin_required

router = APIRouter(prefix='/reports', tags=['reports'])

@router.get('/health', dependencies=[Depends(admin_required)])
def health():
    return {"ok": True}
