from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from ..deps import admin_required
from ..models import Employee

router = APIRouter(prefix='/employees', tags=['employees'])

class EmpIn(BaseModel):
    name: str
    designation: str | None = None
    department: str | None = None
    doj: str | None = None
    base_salary: float = 0.0
    is_active: bool = True

class EmpOut(BaseModel):
    id: int
    name: str
    designation: str | None
    department: str | None
    doj: str | None
    base_salary: float
    is_active: bool

@router.get('/', response_model=List[EmpOut], dependencies=[Depends(admin_required)])
def list_employees():
    return [EmpOut(id=e.id, name=e.name, designation=e.designation, department=e.department,
                   doj=str(e.doj) if e.doj else None, base_salary=e.base_salary, is_active=e.is_active)
            for e in Employee.select().order_by(Employee.id.desc())]

@router.post('/', dependencies=[Depends(admin_required)])
def create_employee(data: EmpIn):
    e = Employee.create(name=data.name, designation=data.designation, department=data.department,
                        doj=data.doj, base_salary=data.base_salary, is_active=data.is_active)
    return {"ok": True, "id": e.id}

@router.put('/{emp_id}', dependencies=[Depends(admin_required)])
def update_employee(emp_id: int, data: EmpIn):
    e = Employee.get_or_none(Employee.id == emp_id)
    if not e:
        raise HTTPException(status_code=404, detail="Not Found")
    e.name = data.name
    e.designation = data.designation
    e.department = data.department
    e.doj = data.doj
    e.base_salary = data.base_salary
    e.is_active = data.is_active
    e.save()
    return {"ok": True}

@router.delete('/{emp_id}', dependencies=[Depends(admin_required)])
def delete_employee(emp_id: int):
    e = Employee.get_or_none(Employee.id == emp_id)
    if not e:
        raise HTTPException(status_code=404, detail="Not Found")
    e.delete_instance(recursive=True)
    return {"ok": True}
