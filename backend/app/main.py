import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import (
    Column,
    DateTime,
    func,
    Field,
    Session,
    SQLModel,
    select,
)

from app.db import get_db_engine

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "AIPEX2025")


class ResultBase(SQLModel):
    origin: str = Field(max_length=100, index=True)
    label: str = Field(max_length=100, index=True)
    value: float


class Result(ResultBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    last_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime,
            nullable=False,
            onupdate=func.now(),
        ),
    )


class ResultCreate(ResultBase):
    pass


class ResultPublic(ResultBase):
    id: int
    last_updated: datetime


engine = get_db_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/results/", response_model=ResultPublic)
def create_result(
    result: ResultCreate,
    session: SessionDep,
    access_token: Annotated[str | None, Header()] = None,
):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Missing access token")
    if access_token != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid access token")
    db_result = Result.model_validate(result)
    existing_result = session.exec(
        select(Result).where(
            Result.origin == db_result.origin,
            Result.label == db_result.label,
        )
    ).first()
    if existing_result:
        existing_result.value = db_result.value
        session.add(existing_result)
        session.commit()
        session.refresh(existing_result)
        return existing_result
    else:
        session.add(db_result)
        session.commit()
        session.refresh(db_result)
        return db_result


@app.get("/results/", response_model=list[ResultPublic])
def read_results(
    session: SessionDep,
    label: str | None = None,
    maxAgeMin: int = 30,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    statement = select(Result)
    if label is not None:
        statement = statement.where(Result.label == label)
    if maxAgeMin is not None:
        max_age = datetime.now(timezone.utc) - timedelta(minutes=maxAgeMin)
        statement = statement.where(Result.last_updated >= max_age)
    results = session.exec(
        statement.order_by(Result.origin).offset(offset).limit(limit)
    )
    return results


@app.get("/results/{result_id}", response_model=ResultPublic)
def read_result(result_id: int, session: SessionDep):
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@app.delete("/results/{result_id}")
def delete_result(
    result_id: int,
    session: SessionDep,
    access_token: Annotated[str | None, Header()] = None,
):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Missing access token")
    if access_token != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid access token")
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    session.delete(result)
    session.commit()
    return {"ok": True}
