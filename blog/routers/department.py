from fastapi import APIRouter
from fastapi import  Depends, status, HTTPException
from .. import models
from .. import schemas
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from datetime import date

router = APIRouter()




@router.post('/department',tags=['Department'])
def create_department(request:schemas.Department,db:Session=Depends(get_db)):
    new_dept=models.Department(dept_id=request.dept_id,dept_name=request.dept_name)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept




@router.delete('/department/{dep_id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Department'])
def del_dept(dep_id,db:Session=Depends(get_db)):
    dep=db.query(models.Department).filter(models.Department.dept_id==dep_id)
    if not dep.first():
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Department with id {dep_id} not fount")

    dep.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/department/{dep_id}',status_code=status.HTTP_202_ACCEPTED,tags=['Department'])
def update_dept(dep_id,request:schemas.Department, db:Session=Depends(get_db)):
     db.query(models.Department).filter(models.Department.dept_id==dep_id).update(request)
     db.commit()
     return 'updated'


@router.get('/department',tags=['Department'])
async def show_Alldepartment(db:Session=Depends(get_db)):
    all_depts=db.query(models.Department).all()
    return all_depts