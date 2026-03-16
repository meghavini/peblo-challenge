from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChunkResponse(BaseModel):
    source_id: str
    chunk_id: str
    grade: Optional[int]
    subject: Optional[str]
    topic: Optional[str]
    text: str
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question: str
    type: str
    options: Optional[List[str]] = []
    answer: str
    difficulty: str
    topic: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: str  # id is used in user API logic vs expected format
    chunk_id: str
    
    class Config:
        from_attributes = True

class QuizQuestionResponse(BaseModel):
    question_id: str = Field(alias="id") # alias the db id to question_id
    question: str
    options: Optional[List[str]] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class StudentAnswerSubmit(BaseModel):
    student_id: str
    question_id: str
    selected_answer: str

class StudentAnswerResponse(BaseModel):
    id: str
    student_id: str
    question_id: str
    selected_answer: str
    is_correct: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True

class StudentProgressResponse(BaseModel):
    student_id: str
    current_difficulty: str
    score: int
    
    class Config:
        from_attributes = True

class GenerateQuizRequest(BaseModel):
    source_id: str
