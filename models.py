from peewee import (
    Model, AutoField, CharField, DateField, DateTimeField, IntegerField, FloatField, ForeignKeyField, TextField, BooleanField
)
from .db import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    password_hash = CharField()
    role = CharField()  # 'admin' or 'fgcuser'

class Employee(BaseModel):
    id = AutoField()
    name = CharField()
    designation = CharField(null=True)
    department = CharField(null=True)
    doj = DateField(null=True)
    base_salary = FloatField(default=0.0)
    is_active = BooleanField(default=True)

class Attendance(BaseModel):
    id = AutoField()
    employee = ForeignKeyField(Employee, backref='attendance', on_delete='CASCADE')
    date = DateField()
    in_time = CharField(null=True)
    out_time = CharField(null=True)
    status = CharField(default='Present')

class Payroll(BaseModel):
    id = AutoField()
    employee = ForeignKeyField(Employee, backref='payroll', on_delete='CASCADE')
    month = CharField()  # 'YYYY-MM'
    gross = FloatField(default=0.0)
    lop = FloatField(default=0.0)
    cl_bonus = FloatField(default=0.0)
    net = FloatField(default=0.0)

class Leave(BaseModel):
    id = AutoField()
    employee = ForeignKeyField(Employee, backref='leaves', on_delete='CASCADE')
    from_date = DateField()
    to_date = DateField()
    reason = TextField(null=True)
    status = CharField(default='pending')  # pending/approved/rejected

class Sale(BaseModel):
    id = AutoField()
    employee = ForeignKeyField(Employee, backref='sales', on_delete='CASCADE')
    month = CharField()
    amount = FloatField(default=0.0)
    bank = CharField(null=True)

class ActivityLog(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='activities', on_delete='SET NULL', null=True)
    module = CharField()
    action = CharField()
    timestamp = DateTimeField()
