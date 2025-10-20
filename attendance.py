from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from ..deps import fgcuser_allowed, admin_required
from ..models import Attendance, Employee
from peewee import fn
import datetime as dt

router = APIRouter(prefix='/attendance', tags=['attendance'])

class AttIn(BaseModel):
    employee_id: int
    date: str
    in_time: str | None = None
    out_time: str | None = None
    status: str = "Present"

class AttOut(BaseModel):
    id: int
    employee_id: int
    date: str
    in_time: str | None
    out_time: str | None
    status: str

@router.post('/', dependencies=[Depends(fgcuser_allowed)])
def upsert_attendance(data: AttIn):
    date_obj = dt.date.fromisoformat(data.date)
    emp = Employee.get_or_none(Employee.id == data.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    rec = Attendance.get_or_none((Attendance.employee == emp) & (Attendance.date == date_obj))
    if rec:
        rec.in_time = data.in_time or rec.in_time
        rec.out_time = data.out_time or rec.out_time
        rec.status = data.status or rec.status
        rec.save()
    else:
        rec = Attendance.create(employee=emp, date=date_obj, in_time=data.in_time, out_time=data.out_time, status=data.status)
    return {"ok": True, "id": rec.id}

@router.get('/by-employee/{employee_id}', response_model=List[AttOut], dependencies=[Depends(fgcuser_allowed)])
def list_by_employee(employee_id: int):
    rows = (Attendance
            .select()
            .where(Attendance.employee == employee_id)
            .order_by(Attendance.date.desc())
            .limit(200))
    return [AttOut(id=r.id, employee_id=r.employee.id, date=str(r.date), in_time=r.in_time, out_time=r.out_time, status=r.status) for r in rows]

@router.get('/summary', dependencies=[Depends(admin_required)])
def summary():
    today = dt.date.today()
    month_prefix = today.strftime("%Y-%m")
    q = (Attendance
         .select(Attendance.employee, fn.COUNT(Attendance.id).alias('days'))
         .where((Attendance.status == 'Present') & (Attendance.date.cast('text').startswith(month_prefix)))
         .group_by(Attendance.employee))
    return [{"employee_id": r.employee.id, "name": r.employee.name, "present_days": r.days} for r in q]
