from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from models import User, Loan

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Test"}


def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
