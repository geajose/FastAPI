from fastapi import APIRouter
from fastapi import  Depends, status, HTTPException
from .. import models
from .. import schemas
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from datetime import date

router = APIRouter()


@router.get('/employee/{emp_id}',tags=['Employee'])
def show(emp_id,db:Session=Depends(get_db)):
    results= db.query(models.Employee).filter(models.Employee.employee_id==emp_id).first()
    return results


@router.put('/employee/{emp_id}',status_code=status.HTTP_202_ACCEPTED,tags=['Employee'])
def update(emp_id,request:schemas.Employee, db:Session=Depends(get_db)):
    db.query(models.Employee).filter(models.Employee.employee_id==emp_id).update(request)
    db.commit()
    return 'updated'

@router.delete('/employee/{emp_id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Employee'])
def destroy(emp_id,db:Session=Depends(get_db)):
    employe=db.query(models.Employee).filter(models.Employee.employee_id==emp_id)
    if not employe.first():
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Employee with id {emp_id} not fount")
    employe.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.post('/employee')
async def create(request:schemas.Employee, db:Session=Depends(get_db)):
    today = date.today()
    new_employee = models.Employee(employee_id = request.employee_id,name = request.name,joining_date = request.joining_date,role = request.role,
    status = request.status,dept_id=request.dept_id,start_date = request.start_date,experience=today.year - request.start_date.year - ((today.month, today.day) < (request.start_date.month, request.start_date.day)),
    address_line1=request.address_line1,address_line2 =request.address_line2,state = request.state,pincode = request.pincode)
    

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee







