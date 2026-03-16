from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Source, Chunk, Question
from app.schemas import GenerateQuizRequest, QuestionResponse, QuizQuestionResponse
from app.services.quiz_generator import generate_questions_for_chunk

router = APIRouter(tags=["Quiz"])

@router.post("/generate-quiz", response_model=List[QuestionResponse])
def generate_quiz(req: GenerateQuizRequest, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == req.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
        
    chunks = db.query(Chunk).filter(Chunk.source_id == req.source_id).all()
    if not chunks:
        raise HTTPException(status_code=404, detail="No chunks found for this source")
        
    generated_questions = []
    
    for chunk in chunks:
        # Check if questions already exist for this chunk to avoid duplicates
        existing_q = db.query(Question).filter(Question.chunk_id == chunk.id).first()
        if existing_q:
            continue
            
        questions_data = generate_questions_for_chunk(chunk.text)
        
        if not questions_data:
            continue
            
        for q_data in questions_data:
            # Safely get variables
            q_text = q_data.get("question")
            q_type = q_data.get("type", "MCQ")
            q_options = q_data.get("options", [])
            q_answer = q_data.get("answer")
            q_difficulty = q_data.get("difficulty", "medium")
            
            if not q_text or not q_answer:
                continue
                
            question = Question(
                chunk_id=chunk.id,
                question=q_text,
                type=q_type,
                options=q_options,
                answer=str(q_answer),
                difficulty=q_difficulty.lower(),
                topic=chunk.topic or chunk.subject
            )
            db.add(question)
            generated_questions.append(question)
            
    db.commit()
    for q in generated_questions:
        db.refresh(q)
    
    return generated_questions

@router.get("/quiz", response_model=List[QuizQuestionResponse])
def get_quiz(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if topic:
        query = query.filter(Question.topic.ilike(f"%{topic}%"))
    if difficulty:
        query = query.filter(Question.difficulty == difficulty.lower())
        
    questions = query.all()
    # Pydantic 2.x alias generator via populate_by_name handles the transformation
    return questions
