from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_session
from sqlmodel import SQLModel, Session
from models import User, Loan

app = FastAPI()


# @app.get("/")
# async def read_root():
#     return {"message": "Test"}


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


def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
