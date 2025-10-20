from ..models import User, Employee
from ..security import hash_password

def seed():
    if not User.select().where(User.username == 'admin').exists():
        User.create(username='admin', password_hash=hash_password('admin@123'), role='admin')
    if not User.select().where(User.username == 'fgcuser').exists():
        User.create(username='fgcuser', password_hash=hash_password('fgcuser@123'), role='fgcuser')
    if not Employee.select().exists():
        Employee.create(name="Sample Employee", designation="Associate", department="Ops", base_salary=25000.0)
