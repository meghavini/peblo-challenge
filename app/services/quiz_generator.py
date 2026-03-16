import json
from google import genai
from google.genai import types
from app.config import settings

client = genai.Client(api_key=settings.LLM_API_KEY)

def generate_questions_for_chunk(chunk_text: str):
    prompt = f"""You are a school teacher.

Generate three quiz questions from the following educational text.

Include:
1 Multiple Choice Question
1 True/False Question
1 Fill in the blank question.

Return structured JSON containing a key "questions" which is an array of question objects. 
Each question object must match this schema exactly:
{{
  "question": "string",
  "type": "MCQ" | "True/False" | "Fill in the blank",
  "options": ["string"] (only for MCQ, otherwise empty array or skip),
  "answer": "string",
  "difficulty": "easy" | "medium" | "hard"
}}

Text:
{chunk_text}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction="You are a helpful assistant designed to output JSON."
            )
        )
        content = response.text
        data = json.loads(content)
        
        # We instructed it to return {"questions": [...]}, handle variations
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
        elif isinstance(data, list):
            return data
            
        return data.get("questions", [])
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        raise ValueError(f"Failed to generate questions: {str(e)}")
