from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "sqlite:///../tweets.db"
# "mysql://root:JZb8Oq4KbQlHCd2rqYok@database-maji.\
# ckdgmsbcegnw.us-east-1.rds.amazonaws.com/database-maji"
# arn:aws:rds:us-east-1:181544540765:db:database-maji


# database_url = "postgresql://user:password@postgresserver/db"

# connect_args only needed for SQLite
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
