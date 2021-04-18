import os

### Postgres Configs ###
POSTGRES_USER = os.environ.get("POSTGRES_USER", "foo")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "bar")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "happyfox")

### SQLAlchemy Config ###
DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
