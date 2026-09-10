from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "backend.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base.metadata.create_all(bind=engine)

# Keep local development databases created before Phase 2 usable.
with engine.connect() as connection:
    columns = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info(conversations)")}
    if "user_id" not in columns:
        connection.exec_driver_sql("ALTER TABLE conversations ADD COLUMN user_id INTEGER")
        connection.commit()

    user_columns = {row[1] for row in connection.exec_driver_sql("PRAGMA table_info(users)")}
    for column, definition in {
        "is_verified": "INTEGER NOT NULL DEFAULT 0",
        "verification_token_hash": "VARCHAR(64)",
        "reset_token_hash": "VARCHAR(64)",
        "reset_token_expires_at": "DATETIME",
    }.items():
        if column not in user_columns:
            connection.exec_driver_sql(f"ALTER TABLE users ADD COLUMN {column} {definition}")
    connection.commit()
