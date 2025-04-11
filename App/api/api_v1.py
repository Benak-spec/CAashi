from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db
from ..utils.security import get_current_user

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.post("/users/{user_id}/budgets/", response_model=schemas.Budget)
def create_budget_for_user(
    user_id: int, budget: schemas.BudgetCreate, db: Session = Depends(get_db)
):
    return crud.create_user_budget(db=db, budget=budget, user_id=user_id)

@router.get("/budgets/", response_model=List[schemas.Budget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budgets = crud.get_budgets(db, skip=skip, limit=limit)
    return budgets