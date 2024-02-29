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


def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
