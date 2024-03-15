from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    loans: List["Loan"] = Relationship(back_populates="owner")


class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: float
    annual_interest_rate: float
    loan_term_months: int
    owner: User = Relationship(back_populates="loans")


class LoanSchedule(SQLModel):
    month: int
    remaining_balance: float
    monthly_payment: float

class LoanSummary(SQLModel):
    total_principal_paid: float
    total_interest_paid: float
    current_principal_balance: float