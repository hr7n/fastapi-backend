from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import engine, get_session
from sqlmodel import SQLModel, Session
from models import User, Loan, LoanSchedule, LoanSummary
from loan_calc import loan_schedule, loan_summary as generate_loan_summary

app = FastAPI()


## Users


@app.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_session)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: User, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


## Loans


@app.post("/loans/", response_model=Loan)
def create_loan(loan: Loan, db: Session = Depends(get_session)):
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@app.get("/loans/{loan_id}", response_model=Loan)
def read_loan(loan_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@app.get(
    "/loans/{loan_id}/schedule",
    response_model=List[LoanSchedule],
)
def get_loan_schedule(loan_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    schedule = loan_schedule(
        loan.amount, loan.annual_interest_rate, loan.loan_term_months
    )

    return schedule


@app.get(
    "/loans/{loan_id}/summary/{month}",
    response_model=LoanSummary,
)
def get_loan_summary(month: int, loan_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    try:
        summary = generate_loan_summary(
            loan.amount, loan.annual_interest_rate, loan.loan_term_months, month
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return summary

@app.get('/users/{user_id}/loans', response_model=List[Loan])
def get_user_loans(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user.loans



def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
