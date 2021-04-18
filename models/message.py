from sqlalchemy import ARRAY, Column, Date, Integer, String

from models.base import engine, Base, Session


class EMail(Base):
    """
    Stores the email metadata
    """

    __tablename__ = "email"
    id = Column(String, primary_key=True)
    sender = Column(String)
    recipient = Column(String)
    date = Column(Date)
    subject = Column(String)
    labels = Column(ARRAY(String))
