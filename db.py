from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

engine = create_engine('sqlite:///hookah.db', echo=True)

Base = declarative_base()


class Clients(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True)
    client_chat_id = Column(Integer)
    client_username = Column(String)
    client_name = Column(String)
    phone_number = Column(String)
    reservation_time = Column(String)
    reservation_day = Column(String)
    amount_of_people = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"
    client_id = Column(Integer, primary_key=True)
    client_chat_id = Column(Integer)
    client_username = Column(String)
    client_name = Column(String)
    feedback = Column(String)


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
