# Mini Content Ingestion + Adaptive Quiz Engine

An AI-powered backend system built with FastAPI that ingests educational content from PDFs, processes the content into chunks, generates quizzes using LLMs (OpenAI/Gemini), stores them using SQLite/SQLAlchemy, and exposes APIs to submit answers with adaptive difficulty formatting.

## System Architecture

PDF Upload -> Text Extraction -> Text Cleaning -> Content Chunking -> Database Storage -> LLM Quiz Generation -> Quiz API -> Student Answer API -> Adaptive Difficulty Logic

## Setup Instructions

1. **Clone the repository or access project folder**
2. **Setup virtual environment** (Optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy the example env file and add your `LLM_API_KEY`:
   ```bash
   cp .env.example .env
   # Edit .env with your Google Gemini / OpenAI API Key and DATABASE_URL
   ```

## How to run the server

Run the following command:
```bash
python -m uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

## API Endpoints and Swagger testing

FastAPI provides an automatic Swagger UI documentation point where you can test all the APIs manually. 
Visit `http://127.0.0.1:8000/docs`.

### Testing Strategy
To thoroughly test the endpoints:
1. Hit `POST /ingest` with a PDF file to extract chunks.
2. Copy the resulting `source_id` to generate questions using `POST /generate-quiz`.
3. View the generated quizzes via `GET /quiz`.
4. Submit answers via `POST /submit-answer` to see Adaptive Difficulty in action.

### Example API Responses

#### 1. POST `/ingest`
- Input: `file` (PDF Upload form data)
- Response: 
```json
{
  "message": "Successfully ingested sample.pdf into 5 chunks.",
  "source_id": "8b3f2...a12c"
}
```

#### 2. POST `/generate-quiz`
- Input:
```json
{
  "source_id": "8b3f2...a12c"
}
```
- Response:
```json
{
  "message": "Generated 15 new questions for source 8b3f2...a12c."
}
```

#### 3. GET `/quiz?topic=math&difficulty=easy`
- Response:
```json
[
  {
    "question": "How many sides does a triangle have?",
    "type": "MCQ",
    "options": ["2", "3", "4", "5"],
    "answer": "3",
    "difficulty": "easy",
    "topic": "math",
    "id": "q_abc123",
    "chunk_id": "ch_def456"
  }
]
```

#### 4. POST `/submit-answer`
- Input:
```json
{
  "student_id": "S001",
  "question_id": "q_abc123",
  "selected_answer": "3"
}
```
- Response:
```json
{
  "id": "ans_xyz789",
  "student_id": "S001",
  "question_id": "q_abc123",
  "selected_answer": "3",
  "is_correct": true,
  "timestamp": "2023-10-25T12:00:00Z"
}
```

#### 5. GET `/student-progress?student_id=S001`
- Response:
```json
{
  "student_id": "S001",
  "current_difficulty": "medium",
  "score": 1
}
```
