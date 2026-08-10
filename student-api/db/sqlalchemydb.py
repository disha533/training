# db/sqlalchemydb.py
#
# SQLAlchemy engine/session for NEW tables only.
# Does not touch db/oracle.py or the STUDENTS table in any way —
# this is a second, independent connection path to the same Oracle DB.

from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import DB_USER, DB_PASSWORD, DB_DSN

host_port, service_name = DB_DSN.split("/")

DATABASE_URL = (
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{host_port}/"
    f"?service_name={service_name}"
)

engine = create_engine(DATABASE_URL, pool_size=2, max_overflow=8, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable dependency alias — bundles "give me a Session" + "how to get one"
# into a single type, so controllers just write `db: SessionDep` instead of
# repeating `db: Session = Depends(get_db)` on every route.
SessionDep = Annotated[Session, Depends(get_db)]