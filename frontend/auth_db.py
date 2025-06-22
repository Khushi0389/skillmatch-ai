# frontend/auth_db.py
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib

DATABASE_URL = "sqlite:///frontend/users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

# History model
class ResumeHistory(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"))
    skills = Column(Text)
    score = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Auth Utils
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        db.close()
        return False
    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    db.close()
    return True

def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user and user.password == hash_password(password)

# History Utils
def save_history(username, skills, score):
    db = SessionLocal()
    record = ResumeHistory(username=username, skills=", ".join(skills), score=str(score))
    db.add(record)
    db.commit()
    db.close()

def get_user_history(username):
    db = SessionLocal()
    records = db.query(ResumeHistory).filter(ResumeHistory.username == username).order_by(ResumeHistory.date.desc()).all()
    db.close()
    return records


def delete_history_entry(entry_id):
    db = SessionLocal()
    record = db.query(ResumeHistory).filter(ResumeHistory.id == entry_id).first()
    if record:
        db.delete(record)
        db.commit()
    db.close()
