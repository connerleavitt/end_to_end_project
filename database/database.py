from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .database_secrets import db_name, host, password, port, username

# database_url = "sqlite:///../tweets.db"
database_url = (
    "mysql://" + username + ":" + password + "@" + host + ":" + port + "/" + db_name
)

# connect_args only needed for SQLite
# engine = create_engine(database_url, connect_args={"check_same_thread": False})
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
