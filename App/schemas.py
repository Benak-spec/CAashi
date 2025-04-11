from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class BudgetBase(BaseModel):
    name: str
    amount: float


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    user_id: int
    categories: List['BudgetCategory']

    class Config:
        orm_mode = True


class BudgetCategoryBase(BaseModel):
    name: str
    allocated_amount: float


class BudgetCategoryCreate(BudgetCategoryBase):
    pass


class BudgetCategory(BudgetCategoryBase):
    id: int
    spent_amount: float
    budget_id: int

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: datetime
    category: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True