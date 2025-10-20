from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import db
from .models import User, Employee, Attendance, Payroll, Leave, Sale, ActivityLog
from .utils.seed import seed
from .routers import users, attendance, employees, payroll, leave, sales, reports

app = FastAPI(title="Fincore HRMS Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Employee, Attendance, Payroll, Leave, Sale, ActivityLog])
    seed()

@app.on_event("shutdown")
def on_shutdown():
    if not db.is_closed():
        db.close()

@app.get("/api/health")
def health():
    return {"status": "ok"}

app.include_router(users.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(employees.router, prefix="/api")
app.include_router(payroll.router, prefix="/api")
app.include_router(leave.router, prefix="/api")
app.include_router(sales.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
