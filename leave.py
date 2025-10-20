from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..deps import admin_required, fgcuser_allowed
from ..models import Leave, Employee

router = APIRouter(prefix='/leave', tags=['leave'])

class LeaveIn(BaseModel):
    employee_id: int
    from_date: str
    to_date: str
    reason: str | None = None

@router.post('/apply', dependencies=[Depends(fgcuser_allowed)])
def apply(data: LeaveIn):
    emp = Employee.get_or_none(Employee.id == data.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    rec = Leave.create(employee=emp, from_date=data.from_date, to_date=data.to_date, reason=data.reason, status='pending')
    return {"ok": True, "id": rec.id}

@router.post('/approve/{leave_id}', dependencies=[Depends(admin_required)])
def approve(leave_id: int):
    rec = Leave.get_or_none(Leave.id == leave_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not Found")
    rec.status = 'approved'; rec.save()
    return {"ok": True}

@router.post('/reject/{leave_id}', dependencies=[Depends(admin_required)])
def reject(leave_id: int):
    rec = Leave.get_or_none(Leave.id == leave_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not Found")
    rec.status = 'rejected'; rec.save()
    return {"ok": True}

@router.get('/list', dependencies=[Depends(admin_required)])
def list_all():
    rows = Leave.select().order_by(Leave.id.desc())
    return [{"id": r.id, "emp": r.employee.id, "from": str(r.from_date), "to": str(r.to_date), "status": r.status, "reason": r.reason} for r in rows]
