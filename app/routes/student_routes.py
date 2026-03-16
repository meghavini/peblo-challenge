from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Question, StudentAnswer, StudentProgress
from app.schemas import StudentAnswerSubmit, StudentAnswerResponse, StudentProgressResponse
from app.services.adaptive_engine import adjust_difficulty

router = APIRouter(tags=["Student"])

@router.post("/submit-answer", response_model=StudentAnswerResponse)
def submit_answer(req: StudentAnswerSubmit, db: Session = Depends(get_db)):
    # 1. Retrieve correct answer
    question = db.query(Question).filter(Question.id == req.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    # 2. Compare with student answer
    is_correct = (str(req.selected_answer).strip().lower() == str(question.answer).strip().lower())
    
    # 3. Save result
    student_ans = StudentAnswer(
        student_id=req.student_id,
        question_id=req.question_id,
        selected_answer=req.selected_answer,
        is_correct=is_correct
    )
    db.add(student_ans)
    
    # 4. Update student performance and Adjust difficulty
    progress = db.query(StudentProgress).filter(StudentProgress.student_id == req.student_id).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=req.student_id,
            current_difficulty="easy",
            score=0
        )
        db.add(progress)
    
    progress.score += 1 if is_correct else 0
    progress.current_difficulty = adjust_difficulty(progress.current_difficulty, is_correct)
    
    db.commit()
    db.refresh(student_ans)
    
    return student_ans

@router.get("/student-progress", response_model=StudentProgressResponse)
def get_student_progress(student_id: str, db: Session = Depends(get_db)):
    progress = db.query(StudentProgress).filter(StudentProgress.student_id == student_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Student progress not found")
        
    return progress
