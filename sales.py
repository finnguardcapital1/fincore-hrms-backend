from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..deps import admin_required
from ..models import Sale, Employee

router = APIRouter(prefix='/sales', tags=['sales'])

class SaleIn(BaseModel):
    employee_id: int
    month: str
    amount: float
    bank: str | None = None

@router.post('/', dependencies=[Depends(admin_required)])
def add_sale(data: SaleIn):
    emp = Employee.get_or_none(Employee.id == data.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    rec = Sale.create(employee=emp, month=data.month, amount=data.amount, bank=data.bank)
    return {"ok": True, "id": rec.id}

@router.get('/by-employee/{emp_id}', dependencies=[Depends(admin_required)])
def by_employee(emp_id: int):
    rows = Sale.select().where(Sale.employee == emp_id).order_by(Sale.month.desc())
    return [{"id": r.id, "month": r.month, "amount": r.amount, "bank": r.bank} for r in rows]
