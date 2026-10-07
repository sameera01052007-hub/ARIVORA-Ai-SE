from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ============================================================
# ARIVORA AI - DATA SCHEMAS & MODELS
# ============================================================

class UserProfile(BaseModel):
    name: str
    role: str = "student"
    education: str = "College"
    board: str = "Anna University"
    institution: str = ""
    medium: str = "English"
    course: str = "B.E / B.Tech"
    branch: str = "Computer Science and Engineering"
    languages: List[str] = ["English", "Tamil"]

class FolderCreateRequest(BaseModel):
    folder_name: str
    username: str = "Student"
    role: str = "student"

class ChatRequest(BaseModel):
    message: str
    subject: str = ""
    language: str = "English"
    username: str = "Student"

class AnswerRequest(BaseModel):
    topic: str
    subject: str = ""
    marks: int = Field(default=5, description="Exam marks rubric: 2, 5, 10, or 16")
    language: str = Field(default="English", description="English, Tamil, or Thanglish")
    username: str = "Student"

class ReferenceRequest(BaseModel):
    topic: str
    subject: str = ""
    username: str = "Student"

class QuizRequest(BaseModel):
    topic: str
    subject: str = ""
    number_of_questions: int = 5
    language: str = "English"
    difficulty: str = "Medium"

class QuizSubmitRequest(BaseModel):
    topic: str
    subject: str = ""
    answers: Dict[int, str]
    username: str = "Student"

class ExamRequest(BaseModel):
    exam_name: str
    exam_date: str
    subject: str = ""
    username: str = "Student"

class FacultyRequest(BaseModel):
    topic: str
    content_type: str = "seminar"  # seminar, lecture, questions, answer_key
    language: str = "English"
    subject: str = ""
    marks: Optional[int] = 16

class SyllabusCheckRequest(BaseModel):
    topic: str
    subject: str = ""

class VoiceTTSRequest(BaseModel):
    text: str
    language: str = "en"  # "en" or "ta"
    username: str = "Student"

class PYQFilterRequest(BaseModel):
    university: str = "Anna University"
    subject: str = ""
    year: Optional[int] = None
    marks: Optional[int] = None
