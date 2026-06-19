from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT,
    DATABASE_URL
)


def get_database_url():
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            return DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        return DATABASE_URL

    return (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


SQLALCHEMY_DATABASE_URL = get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()