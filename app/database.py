import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    postgres_db = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")

    if postgres_db and postgres_user and postgres_password:
        return (
            f"postgresql+psycopg://{postgres_user}:{postgres_password}@"
            f"{postgres_host}:{postgres_port}/{postgres_db}"
        )

    return "sqlite:///./mnemora.db"


def should_use_sqlite() -> bool:
    return get_database_url().startswith("sqlite")


engine = create_engine(
    get_database_url(),
    connect_args={"check_same_thread": False} if should_use_sqlite() else {},
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
