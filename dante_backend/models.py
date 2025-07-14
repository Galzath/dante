from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./dante.db"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    encrypted_token = Column(Text)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    field = Column(String)  # e.g., "sender", "subject"
    condition = Column(String)  # e.g., "CONTAINS", "STARTS_WITH"
    value = Column(String)

class UnreadEmail(Base):
    __tablename__ = "unread_emails"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    category = Column(String, index=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
