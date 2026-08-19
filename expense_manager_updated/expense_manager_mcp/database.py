from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from expense_manager_mcp.config import Settings
from expense_manager_mcp.models import Base


def build_oracle_url(settings: Settings) -> str:
    return (
        f"oracle+oracledb://{settings.oracle_user}:{settings.oracle_password}"
        f"@{settings.oracle_host}:{settings.oracle_port}"
        f"/?service_name={settings.oracle_service_name}"
    )


def create_session_factory(settings: Settings | None = None) -> sessionmaker[Session]:
    s = settings or Settings()
    engine = create_engine(build_oracle_url(s), pool_pre_ping=True, future=True)
    return sessionmaker(bind=engine, expire_on_commit=False)


def create_tables(settings: Settings | None = None) -> None:
    s = settings or Settings()
    engine = create_engine(build_oracle_url(s), future=True)
    Base.metadata.create_all(engine)
