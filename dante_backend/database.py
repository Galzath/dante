import os
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from . import models

# Load encryption key from environment variable
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("No ENCRYPTION_KEY set for Flask application")
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_token(token):
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token):
    return fernet.decrypt(encrypted_token.encode()).decode()

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    models.create_tables()

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, encrypted_token: str):
    db_user = models.User(email=email, encrypted_token=encrypted_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_rules(db: Session):
    return db.query(models.Rule).all()

def add_unread_email(db: Session, message_id: str, category: str):
    db_email = models.UnreadEmail(message_id=message_id, category=category)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def get_unread_emails_by_category(db: Session, category: str):
    return db.query(models.UnreadEmail).filter(models.UnreadEmail.category == category).all()

def delete_unread_emails_by_category(db: Session, category: str):
    db.query(models.UnreadEmail).filter(models.UnreadEmail.category == category).delete()
    db.commit()
