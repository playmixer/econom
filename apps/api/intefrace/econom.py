from pydantic import BaseModel
from typing import List
from datetime import datetime
from apps.econom import models


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
