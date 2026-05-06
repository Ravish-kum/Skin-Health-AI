from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    phone = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    image_uploads = relationship("ImageUpload", back_populates="user")
    progress_trackings = relationship("ProgressTracking", back_populates="user")

class ImageUpload(Base):
    __tablename__ = 'image_uploads'
    image_id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(500))
    upload_date = Column(DateTime, default=datetime.utcnow)
    body_part = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True) # Optional if not logged in

    user = relationship("User", back_populates="image_uploads")
    diagnosis = relationship("Diagnosis", back_populates="image_upload", uselist=False)

class Diagnosis(Base):
    __tablename__ = 'diagnoses'
    diagnosis_id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(255))
    confidence_score = Column(Float)
    description = Column(Text, nullable=True)
    precautions = Column(Text, nullable=True)
    diagnosis_date = Column(DateTime, default=datetime.utcnow)
    image_id = Column(Integer, ForeignKey('image_uploads.image_id'))

    image_upload = relationship("ImageUpload", back_populates="diagnosis")
    progress_trackings = relationship("ProgressTracking", back_populates="diagnosis")
    chats = relationship("AIChat", back_populates="diagnosis")

class ProgressTracking(Base):
    __tablename__ = 'progress_trackings'
    progress_id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey('diagnoses.diagnosis_id'))
    status = Column(String(100)) # E.g. Improving/Same/Worse
    notes = Column(Text, nullable=True)
    progress_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)

    diagnosis = relationship("Diagnosis", back_populates="progress_trackings")
    user = relationship("User", back_populates="progress_trackings")

class AIChat(Base):
    __tablename__ = 'ai_chats'
    chat_id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey('diagnoses.diagnosis_id'))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    diagnosis = relationship("Diagnosis", back_populates="chats")
