# Peblo Content Ingestion & Adaptive Quiz Engine

An AI-powered backend system built with FastAPI that ingests educational content from PDFs, processes the content into meaningful chunks, generates quizzes using LLMs (Google Gemini), stores them using SQLite/SQLAlchemy, and exposes APIs to submit answers with adaptive difficulty formatting. This project was developed as part of the Peblo AI Backend Engineer Challenge.

## System Architecture & Data Flow

**PDF Upload** -> **Text Extraction** -> **Text Cleaning** -> **Content Chunking** -> **Database Storage** -> **LLM Quiz Generation** -> **Quiz API Retrieval** -> **Student Answer Submission** -> **Adaptive Difficulty Logic**

- **Ingestion**: Uploaded PDFs are parsed via `pdfplumber`, cleaned of null bytes, and chunked into roughly 200-word segments to remain concise without losing context.
- **Data Modeling**: The system utilizes a generic relational `SQLite` database powered by SQLAlchemy. The schemas represent a `Source` (Document) -> `Chunk` (Segment) -> `Question` (Generated entities) hierarchy, ensuring complete traceability.
- **AI Integration**: The system natively leverages `google-genai` and the `gemini-2.0-flash` model which restricts out-of-bounds generation by exclusively returning strict JSON structures requested in the standard prompt.
- **Adaptive Engine**: Difficulty progresses logically (e.g. `easy` -> `medium` -> `hard`) upon submitting correct Student Answers linked to specific Question IDs.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed on your machine.

### 2. Clone the Repository
Clone the project or open the folder in your terminal:
```bash
git clone https://github.com/meghavini/peblo-challenge.git
cd peblo-challenge
```

### 3. Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the `.env.example` file to create your local `.env` configuration.
```bash
cp .env.example .env
```
Inside the `.env` file, replace `your_api_key_here` with a valid Google Gemini API Key from Google AI Studio. 
*(Note: A valid API key with active quota limits is strictly required for Quiz Generation to operate without throwing an Internal Server Error).*

### 6. Run the Backend Server
```bash
python -m uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`. Database tables (`quiz.db`) will be initialized automatically upon the first successful run.

## API Endpoints & Testing Instructions

FastAPI provides an automatic Swagger UI documentation point where you can test all the APIs manually without a frontend!
Visit `http://127.0.0.1:8000/docs`.

### Testing Strategy flow:
1. Hit `POST /ingest` with a PDF file (e.g. `peblo_pdf_grade1_math_numbers.pdf`) to extract chunks.
2. Copy the resulting `source_id` from the response.
3. Paste the `source_id` into the JSON payload for `POST /generate-quiz` to trigger Google Gemini to generate MCQs, True/False, and fill-in-the-blank questions.
4. View the generated quizzes via `GET /quiz`. You can filter by `topic` and `difficulty`.
5. Submit answers via `POST /submit-answer` to evaluate student correctness and witness Adaptive Difficulty in action. Check `GET /student-progress` using the same `student_id`.

## Sample Outputs

### 1. Extracted JSON Content (`POST /ingest`)
```json
{
  "message": "Successfully ingested peblo_pdf_grade1_math_numbers.pdf into 1 chunks.",
  "source_id": "f3239c64-6cae-477a-ab1e-fd79d1407de3"
}
```

### 2. Generated Quiz Questions API (`GET /quiz`)
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

### 3. Student Submission Adaptive Response (`POST /submit-answer`)
```json
{
  "id": "ans_xyz789",
  "student_id": "S001",
  "question_id": "q_abc123",
  "selected_answer": "3",
  "is_correct": true,
  "timestamp": "2026-03-25T12:00:00Z"
}
```

## Demo Video Walkthrough

🎥 **Video Link]**

