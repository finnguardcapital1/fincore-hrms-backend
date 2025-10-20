from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..deps import admin_required
from ..models import Payroll, Employee

router = APIRouter(prefix='/payroll', tags=['payroll'])

class PayrollIn(BaseModel):
    employee_id: int
    month: str  # 'YYYY-MM'
    gross: float = 0.0
    lop: float = 0.0
    cl_bonus: float = 0.0

@router.post('/generate', dependencies=[Depends(admin_required)])
def generate(data: PayrollIn):
    emp = Employee.get_or_none(Employee.id == data.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    net = data.gross - data.lop + data.cl_bonus
    rec, created = Payroll.get_or_create(employee=emp, month=data.month, defaults={
        "gross": data.gross, "lop": data.lop, "cl_bonus": data.cl_bonus, "net": net
    })
    if not created:
        rec.gross = data.gross; rec.lop = data.lop; rec.cl_bonus = data.cl_bonus; rec.net = net; rec.save()
    return {"ok": True, "id": rec.id, "net": rec.net}

@router.get('/by-employee/{emp_id}', dependencies=[Depends(admin_required)])
def by_employee(emp_id: int):
    rows = Payroll.select().where(Payroll.employee == emp_id).order_by(Payroll.month.desc())
    return [{"id": r.id, "month": r.month, "gross": r.gross, "lop": r.lop, "cl_bonus": r.cl_bonus, "net": r.net} for r in rows]
