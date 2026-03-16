import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Source(Base):
    __tablename__ = "sources"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    file_name = Column(String, index=True)
    grade = Column(Integer, nullable=True)
    subject = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chunks = relationship("Chunk", back_populates="source", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    source_id = Column(String, ForeignKey("sources.id"))
    topic = Column(String, nullable=True)
    grade = Column(Integer, nullable=True)
    subject = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    
    source = relationship("Source", back_populates="chunks")
    questions = relationship("Question", back_populates="chunk", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    chunk_id = Column(String, ForeignKey("chunks.id"))
    question = Column(String, nullable=False)
    type = Column(String, nullable=False)  # MCQ, True/False, Fill in the blank
    options = Column(JSON, nullable=True)
    answer = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)  # easy, medium, hard
    topic = Column(String, nullable=True)
    
    chunk = relationship("Chunk", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    student_id = Column(String, index=True)
    question_id = Column(String, ForeignKey("questions.id"))
    selected_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    question = relationship("Question", back_populates="answers")

class StudentProgress(Base):
    __tablename__ = "student_progress"
    student_id = Column(String, primary_key=True, index=True)
    current_difficulty = Column(String, default="easy")
    score = Column(Integer, default=0)
