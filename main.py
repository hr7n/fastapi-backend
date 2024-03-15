from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import engine, get_session
from sqlmodel import SQLModel, Session
from models import User, Loan, LoanSchedule, LoanSummary, UserLoanLink
from loan_calc import loan_schedule, loan_summary as generate_loan_summary

app = FastAPI()

## Users

# Create user
@app.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_session)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Get user by id
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by id
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

# Delete user
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


## Loans

# Create loan
@app.post("/loans/", response_model=Loan)
def create_loan(loan: Loan, db: Session = Depends(get_session)):
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

# Get loan by id
@app.get("/loans/{loan_id}", response_model=Loan)
def read_loan(loan_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

# Get loan schedule
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

# Get loan summary
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

# Get user loans
@app.get('/users/{user_id}/loans', response_model=List[Loan])
def get_user_loans(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user.loans

# Share loan with another user
@app.post('/loans/{loan_id}/share/{user_id}')
def share_loan_with_user(loan_id: int, user_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_link = db.query(UserLoanLink).filter(UserLoanLink.user_id == user.id, UserLoanLink.loan_id == loan.id).first()
    if existing_link:
        raise HTTPException(status_code=404, detail="Loan already shared with this user")

    new_link = UserLoanLink(user_id=user_id, loan_id=loan_id)
    db.add(new_link)
    db.commit()

    return {"message": "Loan shared successfully"}

# Get users for loan
@app.get('/loans/{loan_id}/users', response_model=List[User])
def get_users_for_loan(loan_id: int, db: Session = Depends(get_session)):
    loan = db.get(Loan, loan_id)
    if not loan: raise HTTPException(status_code=404, detail="Loan not found")

    user_links = db.query(UserLoanLink).filter(UserLoanLink.loan_id == loan.id).all()
    user_ids = [link.user_id for link in user_links]
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    return users

def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
