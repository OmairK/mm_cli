from sqlalchemy import ARRAY, Column, Date, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.db_configs import DATABASE_URI

engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class EMail(Base):
    """
    Stores the email metadata
    """
    __tablename__ = "email"
    message_id = Column(String, primary_key=True)
    sender = Column(String)
    recipient = Column(String)
    date = Column(Date)
    subject = Column(String)
    labels = Column(ARRAY(String))
