from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


class Wallet(BaseModel):
    id: int
    title: str
    balance: float


class Income(BaseModel):
    id: int
    title: str
    money: float
    wallet_id: int
    time_event: datetime


class Expense(BaseModel):
    id: int
    title: str
    money: float
    wallet_id: int
    time_event: datetime


class Action(BaseModel):
    id: Optional[int]
    title: Optional[str]
    money: Optional[float]
    wallet_id: Optional[int]
    time_event: Optional[date]
