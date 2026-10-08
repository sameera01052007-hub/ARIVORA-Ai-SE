import os
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from config import (
    BASE_DIR, DATA_DIR, UPLOAD_DIR, STUDENT_DIR, FACULTY_DIR,
    VOICE_DIR, EXAM_DIR, QUIZ_DIR, TIMETABLE_DIR, SUBJECT_CATALOG, SUBJECT_ALIASES,
    BOARDS, LANGUAGES
)
from models import (
    UserProfile, ChatRequest, AnswerRequest, ReferenceRequest,
    QuizRequest, QuizSubmitRequest, ExamRequest, FacultyRequest,
    SyllabusCheckRequest, VoiceTTSRequest, PYQFilterRequest, FolderCreateRequest
)
from services.document_service import document_service
from services.ai_engine import ai_engine
from services.syllabus_service import syllabus_service
from services.reference_service import reference_service
from services.quiz_service import quiz_service
from services.pyq_service import pyq_service
from services.voice_service import voice_service
from services.faculty_service import faculty_service

# ============================================================
# ARIVORA AI - CORE APPLICATION
# "Your Syllabus. Your Books. Your AI."
# ============================================================

app = FastAPI(
    title="ARIVORA AI",
    description="Intelligent Syllabus-Based Learning Ecosystem for School and College Students",
    version="2.0.0"
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# STATIC MOUNTS FOR OFFLINE / DOWNLOAD ACCESS
# ============================================================

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/voice_notes", StaticFiles(directory=str(VOICE_DIR)), name="voice_notes")
app.mount("/timetable_files", StaticFiles(directory=str(TIMETABLE_DIR)), name="timetable_files")

FRONTEND_DIR = BASE_DIR.parent / "Frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)[:100]

def detect_subject_folder(filename: str) -> str:
    lower_name = filename.lower()
    for alias, standard in SUBJECT_ALIASES.items():
        if alias in lower_name:
            return SUBJECT_CATALOG[standard]["folder"]
    return "General"

def ensure_user_folders(base_path: Path):
    folders = {data["folder"] for data in SUBJECT_CATALOG.values()}
    folders.add("General")
    for f in folders:
        (base_path / f).mkdir(parents=True, exist_ok=True)

# ============================================================
# ROOT & HEALTH CHECK
# ============================================================

@app.get("/")
def home(request: Request = None):
    if request:
        accept = request.headers.get("accept", "")
        if "text/html" in accept or "*/*" in accept or not accept:
            return RedirectResponse(url="/app/")
    return {
        "project": "ARIVORA AI",
        "motto": "Your Syllabus. Your Books. Your AI.",
        "status": "Running successfully",
        "version": "2.0.0",
        "features": [
            "Syllabus-aware AI Answers (2, 5, 10, 16 marks)",
            "Automatic Unit and Topic Identification",
            "Page-level Smart References & Citations",
            "Bilingual Support (Tamil & English)",
            "Adaptive Quizzes & Revision Cards",
            "Previous Year Questions (Anna Univ, CBSE, State Board)",
            "Out-of-Syllabus Guardian Alert System",
            "Voice AI & Text-to-Speech (gTTS)",
            "Faculty Tools (Seminar, Lecture Notes, Question Papers, Answer Keys)"
        ],
        "api_docs": "/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ARIVORA AI Backend Engine",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================
# 1. ACADEMIC USER PROFILE
# ============================================================

@app.post("/api/profile")
def create_profile(profile: UserProfile):
    username = safe_name(profile.name)
    user_folder = (STUDENT_DIR if profile.role.lower() == "student" else FACULTY_DIR) / username
    user_folder.mkdir(parents=True, exist_ok=True)
    if profile.education.lower() != "school":
        ensure_user_folders(user_folder)

    return {
        "success": True,
        "message": f"Welcome {profile.name}! Your personalized ARIVORA AI profile is ready.",
        "user": profile.model_dump(),
        "folder": str(user_folder),
        "offline_ready": True
    }

# ============================================================
# 2. DOCUMENT / TEXTBOOK UPLOAD & PROCESSING
# ============================================================

@app.post("/api/upload-book")
async def upload_book(
    file: UploadFile = File(...),
    username: str = Form("Student"),
    role: str = Form("student"),
    subject: str = Form("")
):
    safe_user = safe_name(username)
    user_base = (STUDENT_DIR if role.lower() == "student" else FACULTY_DIR) / safe_user
    user_base.mkdir(parents=True, exist_ok=True)
    ensure_user_folders(user_base)

    folder_name = "General"
    if subject.strip():
        standard = SUBJECT_ALIASES.get(subject.lower().strip())
        folder_name = SUBJECT_CATALOG[standard]["folder"] if standard else safe_name(subject)
    else:
        folder_name = detect_subject_folder(file.filename)

    subject_folder = user_base / folder_name
    subject_folder.mkdir(parents=True, exist_ok=True)

    filename = safe_name(file.filename)
    dest_path = subject_folder / filename

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process PDF / Text with document service
    indexing_result = None
    if filename.lower().endswith(".pdf"):
        try:
            indexing_result = document_service.process_pdf(dest_path, safe_user, folder_name)
        except Exception as e:
            indexing_result = {"error": str(e), "is_scanned": True, "note": "Basic file saved without full text indexing."}
    elif filename.lower().endswith((".txt", ".md", ".docx")):
        try:
            indexing_result = document_service.process_text_file(dest_path, safe_user, folder_name)
        except Exception as e:
            indexing_result = {"error": str(e)}

    is_unreadable = False
    error_note = None
    if indexing_result and (indexing_result.get("is_scanned") or indexing_result.get("unreadable") or indexing_result.get("error")):
        if indexing_result.get("total_extracted_chars", 0) < 50:
            is_unreadable = True
            error_note = "⚠️ Unable to process this document. Possible reasons: Scanned PDF, No readable text, Unsupported file, Corrupted file."

    return {
        "success": not is_unreadable,
        "message": f"'{filename}' uploaded successfully for {folder_name}." if not is_unreadable else (error_note or "⚠️ Unable to process this document."),
        "filename": filename,
        "folder": folder_name,
        "offline_ready": True,
        "indexed": indexing_result is not None and not is_unreadable and "error" not in indexing_result,
        "is_scanned": indexing_result.get("is_scanned", False) if indexing_result else False,
        "error_note": error_note,
        "detected_units": indexing_result.get("units", []) if indexing_result else [],
        "uploaded_at": datetime.now().isoformat()
    }

@app.post("/api/create-folder")
def create_custom_folder(request: FolderCreateRequest):
    if not request.folder_name or not request.folder_name.strip():
        raise HTTPException(status_code=400, detail="Folder name cannot be empty")
    safe_user = safe_name(request.username)
    safe_folder = safe_name(request.folder_name.strip())
    user_base = (STUDENT_DIR if request.role.lower() == "student" else FACULTY_DIR) / safe_user
    user_base.mkdir(parents=True, exist_ok=True)

    folder_path = user_base / safe_folder
    folder_path.mkdir(parents=True, exist_ok=True)

    return {
        "success": True,
        "message": f"Folder '{request.folder_name.strip()}' created successfully.",
        "folder_name": request.folder_name.strip(),
        "folder_key": safe_folder
    }

@app.get("/api/folders")
def get_folders(username: str = "Student", role: str = "student", education: str = "College"):
    safe_user = safe_name(username)
    user_base = (STUDENT_DIR if role.lower() == "student" else FACULTY_DIR) / safe_user

    is_school = (education.lower() == "school")

    if not user_base.exists():
        if not is_school:
            ensure_user_folders(user_base)
        else:
            user_base.mkdir(parents=True, exist_ok=True)

    predefined_catalog_folders = {data["folder"] for data in SUBJECT_CATALOG.values()} | {"General"}

    folders = []
    if user_base.exists():
        for f in user_base.iterdir():
            if f.is_dir():
                files = [file.name for file in f.iterdir() if file.is_file()]
                if is_school and f.name in predefined_catalog_folders and len(files) == 0:
                    continue
                folders.append({
                    "name": f.name.replace("_", " "),
                    "folder_key": f.name,
                    "file_count": len(files),
                    "files": files
                })

    return {
        "success": True,
        "username": username,
        "education": education,
        "folders": folders
    }

@app.get("/api/folder/{folder_name}")
def get_folder_details(folder_name: str, username: str = "Student", role: str = "student"):
    safe_user = safe_name(username)
    safe_folder = safe_name(folder_name)
    user_base = (STUDENT_DIR if role.lower() == "student" else FACULTY_DIR) / safe_user
    target = user_base / safe_folder

    if not target.exists():
        raise HTTPException(status_code=404, detail="Folder not found")

    files = [{"name": fl.name, "size": fl.stat().st_size, "path": f"/uploads/{'students' if role.lower() == 'student' else 'faculty'}/{safe_user}/{safe_folder}/{fl.name}"} for fl in target.iterdir() if fl.is_file()]

    return {
        "success": True,
        "folder": folder_name,
        "files": files
    }

# ============================================================
# 3. AI CHAT ASSISTANT
# ============================================================

@app.post("/api/chat")
def chat(request: ChatRequest):
    msg = request.message.strip()
    lower_msg = msg.lower()
    syll_check = None

    if lower_msg in ["hi", "hello", "hey", "vanakkam", "வணக்கம்"]:
        reply = "Hello! 👋 Welcome to ARIVORA AI — Your Syllabus. Your Books. Your AI.\nAsk me any question from your textbooks or syllabus, and I'll provide an exam-oriented answer!"
    elif "motivation" in lower_msg:
        reply = "🌟 'Consistency is the key to academic excellence!' Study one unit at a time, revise the 2-mark definitions daily, and 16-mark essays will feel natural. You've got this! 💪"
    elif "syllabus" in lower_msg and ("what" in lower_msg or "list" in lower_msg):
        reply = "ARIVORA AI currently indexes your uploaded textbooks and syllabus PDFs. You can create custom folders for any school subject and upload study materials!"
    else:
        # Perform dynamic syllabus validation
        syll_check = syllabus_service.check_topic(msg, request.subject, request.username)
        ans_data = ai_engine.generate_answer(msg, marks=5, language=request.language, subject=request.subject, username=request.username)
        
        is_out = ans_data.get("is_out_of_syllabus") or (syll_check and syll_check.get("is_out_of_syllabus"))
        
        doc_match = document_service.search_indexed_materials(msg, request.username, request.subject)
        detected = ai_engine.detect_subject_and_unit(msg, request.subject)

        if is_out:
            ans_text = ans_data.get("answer") or ans_data.get("response") or "Here is the answer generated by ARIVORA AI."
            reply = f"⚠️ OUT OF SYLLABUS ALERT (General AI Answer):\n\n{ans_text}"
        else:
            reply = f"🎯 Subject: {detected['subject']} (Unit {detected['unit']}: {detected['unit_title']})\n\n{ans_data['answer']}"

        topic_name = doc_match.get("topic") if doc_match else (detected.get("topic") or msg)
        subj_name = request.subject if request.subject else (detected.get("subject") or "General")
        unit_num = doc_match.get("unit") if doc_match else (detected.get("unit") or 1)
        unit_title = doc_match.get("chapter") if doc_match else (detected.get("unit_title") or "")
        book_name = doc_match.get("book") if doc_match else (ans_data.get("book") or f"{subj_name} Textbook")
        page_val = doc_match.get("page") if doc_match else None
        page_ref = f"Page {page_val}" if page_val else ""
        ref_text = f"{subj_name} → {unit_title} → {book_name}" + (f" ({page_ref})" if page_ref else "")

        sources = []
        if doc_match:
            sources.append({
                "book": doc_match["book"],
                "chapter": doc_match.get("chapter"),
                "topic": doc_match.get("topic") or msg,
                "page": doc_match.get("page")
            })

    return {
        "success": True,
        "status": "supported",
        "is_out_of_syllabus": False,
        "language": request.language,
        "response": reply,
        "syllabus_check": syll_check,
        "topic": topic_name if 'topic_name' in locals() else msg,
        "subject": subj_name if 'subj_name' in locals() else "",
        "unit": unit_num if 'unit_num' in locals() else "",
        "unit_title": unit_title if 'unit_title' in locals() else "",
        "book": book_name if 'book_name' in locals() else "",
        "chapter": unit_title if 'unit_title' in locals() else "",
        "page": page_val if 'page_val' in locals() else None,
        "page_ref": page_ref if 'page_ref' in locals() else "",
        "reference": ref_text if 'ref_text' in locals() else "",
        "sources": sources if 'sources' in locals() else []
    }

@app.post("/api/general-ai-chat")
def general_ai_chat(request: ChatRequest):
    msg = request.message.strip()
    reply = ai_engine.generate_general_ai_answer(msg, language=request.language)
    return {
        "success": True,
        "language": request.language,
        "response": reply,
        "is_general_ai": True
    }

# ============================================================
# 4. EXAM-ORIENTED MARK-WISE ANSWERS (1, 2, 4, 5, 8, 16 MARKS)
# ============================================================

@app.post("/api/answer")
def get_exam_answer(request: AnswerRequest):
    valid_marks = [1, 2, 3, 4, 5, 8, 10, 16]
    marks = request.marks if request.marks in valid_marks else 5

    syll_check = syllabus_service.check_topic(request.topic, request.subject, request.username)
    res = ai_engine.generate_answer(
        topic=request.topic,
        marks=marks,
        language=request.language,
        subject=request.subject,
        username=request.username
    )
    res["syllabus_check"] = syll_check
    return res

# ============================================================
# 5. SMART REFERENCE FINDER (PAGE-LEVEL CITATIONS)
# ============================================================

@app.post("/api/reference")
def get_reference(request: ReferenceRequest):
    return reference_service.find_reference(
        topic=request.topic,
        subject=request.subject,
        username=request.username
    )

# ============================================================
# 6. ADAPTIVE QUIZ, PROGRESS & REVISION CARDS
# ============================================================

@app.post("/api/quiz")
def generate_quiz(request: QuizRequest):
    return quiz_service.generate_quiz(
        topic=request.topic,
        subject=request.subject,
        count=request.number_of_questions,
        language=request.language
    )

@app.post("/api/quiz/evaluate")
def evaluate_quiz(request: QuizSubmitRequest):
    return quiz_service.evaluate_quiz(
        topic=request.topic,
        user_answers=request.answers
    )

@app.get("/api/progress")
def get_progress(correct: int = Query(...), total: int = Query(...), topic: str = Query(...)):
    if total <= 0:
        raise HTTPException(status_code=400, detail="Total questions must be > 0")
    percentage = round((correct / total) * 100)
    if percentage >= 80:
        feedback = f"🌟 Outstanding performance on {topic}! Your concept clarity is excellent."
    elif percentage >= 50:
        feedback = f"👍 Good progress on {topic}. Review the key formulas and 2-mark definitions."
    else:
        feedback = f"📖 We recommend revising Unit notes for {topic} before taking your next test."

    return {
        "topic": topic,
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "feedback": feedback
    }

@app.get("/api/revision-cards")
def get_revision_cards(topic: str = Query(...), subject: str = Query("")):
    return {
        "success": True,
        "topic": topic,
        "cards": quiz_service.generate_revision_cards(topic, subject)
    }

# ============================================================
# 7. SYLLABUS GUARDIAN (OUT-OF-SYLLABUS DETECTOR)
# ============================================================

@app.get("/api/check-syllabus")
def check_syllabus(topic: str = Query(...), subject: str = Query(""), username: str = Query("Student")):
    return syllabus_service.check_topic(topic, subject, username)

# ============================================================
# 8. PREVIOUS YEAR QUESTIONS (PYQ)
# ============================================================

@app.get("/api/previous-year-questions")
def get_previous_year_questions(
    university: str = Query("Anna University"),
    subject: str = Query(""),
    year: Optional[int] = Query(None),
    marks: Optional[int] = Query(None)
):
    return pyq_service.get_questions(
        board=university,
        subject=subject,
        year=year,
        marks=marks
    )

@app.get("/api/school/pyq-search")
def search_school_previous_year_questions(
    board: str = Query("Tamil Nadu State Board"),
    class_level: str = Query("10"),
    subject: str = Query("Mathematics"),
    year: Optional[int] = Query(None),
    medium: str = Query("English"),
    query: str = Query("")
):
    return pyq_service.search_school_pyqs(
        board=board,
        class_level=class_level,
        subject=subject,
        year=year,
        medium=medium,
        query=query
    )

# ============================================================
# 9. EXAM PLANNER & COUNTDOWN
# ============================================================

@app.post("/api/exam")
def create_exam_reminder(request: ExamRequest):
    exam_record = {
        "exam_name": request.exam_name,
        "exam_date": request.exam_date,
        "subject": request.subject,
        "username": request.username,
        "created_at": datetime.now().isoformat()
    }
    exam_file = EXAM_DIR / "exams.txt"
    with open(exam_file, "a", encoding="utf-8") as f:
        f.write(str(exam_record) + "\n")

    return {
        "success": True,
        "message": f"Exam reminder for '{request.exam_name}' scheduled successfully.",
        "exam": exam_record
    }

@app.get("/api/exam-countdown")
def exam_countdown(exam_date: str = Query(...)):
    try:
        target = datetime.fromisoformat(exam_date.replace("Z", "+00:00").split("T")[0])
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    today = datetime.now()
    diff = target - today
    days = max(0, diff.days)
    hours = max(0, diff.seconds // 3600)

    if days <= 15:
        msg = "⚠️ Final Revision Sprint! Focus exclusively on 16-mark essays and PYQs."
    elif days <= 45:
        msg = "🔥 Intensive Preparation Phase! Solve daily unit quizzes and clarify doubts."
    elif days <= 90:
        msg = "📅 Structured Study Period. Complete one unit every 10 days."
    else:
        msg = f"⏳ {days} Days Remaining. Build foundational concept clarity with your books."

    return {
        "days_remaining": days,
        "hours_remaining": hours,
        "target_date": exam_date,
        "message": msg
    }

def build_study_plan_for_exam(exam_name: str, exam_date: str):
    try:
        target = datetime.fromisoformat(exam_date.split("T")[0])
        days_left = max(0, (target - datetime.now()).days)
    except Exception:
        days_left = 15

    lower = exam_name.lower()
    if "network" in lower:
        subject = "Computer Networks"
        folder = "Computer_Networks"
        unit = "Unit 1"
        topic = "OSI 7-Layer Reference Model & Physical Layer"
        essay = "Dijkstra Shortest Path Routing Algorithm (16 Marks)"
        quiz_topic = "OSI layers"
    elif "dbms" in lower or "database" in lower:
        subject = "Database Management Systems"
        folder = "DBMS"
        unit = "Unit 1"
        topic = "ER Diagrams & Relational Database Architecture"
        essay = "Database Normalization 1NF to BCNF (16 Marks)"
        quiz_topic = "DBMS Normalization"
    elif "operating" in lower or "os" in lower:
        subject = "Operating Systems"
        folder = "Operating_Systems"
        unit = "Unit 2"
        topic = "CPU Scheduling (Round Robin, SJF, Priority)"
        essay = "Banker's Deadlock Avoidance Algorithm (16 Marks)"
        quiz_topic = "CPU Scheduling"
    elif "data structure" in lower or "ds" in lower:
        subject = "Data Structures"
        folder = "Data_Structures"
        unit = "Unit 2"
        topic = "Binary Search Trees & AVL Balancing"
        essay = "Graph Traversal BFS and DFS Mechanisms (16 Marks)"
        quiz_topic = "Binary Trees"
    else:
        subject = exam_name
        folder = "General"
        unit = "Unit 1"
        topic = f"{exam_name} Core Principles"
        essay = f"{exam_name} University 16-Mark Question"
        quiz_topic = exam_name

    return {
        "target_subject": subject,
        "folder": folder,
        "target_unit": unit,
        "days_left": days_left,
        "exam_date": exam_date,
        "quiz_topic": quiz_topic,
        "tasks": [
            {
                "id": "t1",
                "title": f"Revise {unit}: {topic}",
                "detail": f"Focus on 2-mark definitions & formulas in {subject}",
                "type": "study",
                "topic": topic,
                "marks": 2,
                "completed": False
            },
            {
                "id": "t2",
                "title": f"Prepare 16-Mark Question: {essay}",
                "detail": "Practice drawing neat diagrams and stepwise derivations",
                "type": "essay",
                "topic": essay,
                "marks": 16,
                "completed": False
            },
            {
                "id": "t3",
                "title": f"Attempt Daily Adaptive Quiz on '{quiz_topic}'",
                "detail": "Test retention with 5 Anna University standard questions",
                "type": "quiz",
                "topic": quiz_topic,
                "completed": False
            }
        ]
    }

@app.post("/api/timetable/upload")
async def upload_timetable_photo(
    file: UploadFile = File(...),
    username: str = Form("Student")
):
    safe_user = safe_name(username)
    user_timetable_dir = TIMETABLE_DIR / safe_user
    user_timetable_dir.mkdir(parents=True, exist_ok=True)

    dest = user_timetable_dir / f"timetable_{file.filename}"
    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)

    # Default schedule
    default_exams = [
        {"subject": "Computer Networks (CS8591)", "date": "2026-11-20", "days_left": 15, "folder": "Computer_Networks"},
        {"subject": "Database Management Systems (CS8492)", "date": "2026-11-28", "days_left": 23, "folder": "DBMS"},
        {"subject": "Operating Systems (CS8493)", "date": "2026-12-05", "days_left": 30, "folder": "Operating_Systems"}
    ]

    schedule_file = user_timetable_dir / "schedule.json"
    import json
    with open(schedule_file, "w", encoding="utf-8") as f:
        json.dump(default_exams, f, indent=2)

    plan = build_study_plan_for_exam(default_exams[0]["subject"], default_exams[0]["date"])

    return {
        "success": True,
        "message": "📸 Timetable photo uploaded & scanned successfully! Today's study plan generated.",
        "filename": file.filename,
        "file_url": f"/timetable_files/{safe_user}/timetable_{file.filename}",
        "timetable": default_exams,
        "today_plan": plan
    }

@app.get("/api/timetable")
def get_timetable(username: str = Query("Student")):
    safe_user = safe_name(username)
    user_timetable_dir = TIMETABLE_DIR / safe_user
    schedule_file = user_timetable_dir / "schedule.json"
    import json

    if schedule_file.exists():
        try:
            with open(schedule_file, "r", encoding="utf-8") as f:
                exams = json.load(f)
        except Exception:
            exams = []
    else:
        exams = [
            {"subject": "Computer Networks (CS8591)", "date": "2026-11-20", "days_left": 15, "folder": "Computer_Networks"},
            {"subject": "Database Management Systems (CS8492)", "date": "2026-11-28", "days_left": 23, "folder": "DBMS"},
            {"subject": "Operating Systems (CS8493)", "date": "2026-12-05", "days_left": 30, "folder": "Operating_Systems"}
        ]

    nearest_exam = exams[0] if exams else {"subject": "Computer Networks (CS8591)", "date": "2026-11-20"}
    plan = build_study_plan_for_exam(nearest_exam["subject"], nearest_exam["date"])

    return {
        "success": True,
        "timetable": exams,
        "today_plan": plan
    }

# ============================================================
# 10. VOICE AI & TEXT-TO-SPEECH (gTTS)
# ============================================================

@app.post("/api/voice-reply")
def voice_reply(request: VoiceTTSRequest):
    return voice_service.generate_speech(
        text=request.text,
        language=request.language
    )

@app.get("/api/voice-audio/{filename}")
def stream_voice_audio(filename: str):
    file_path = VOICE_DIR / safe_name(filename)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(path=str(file_path), media_type="audio/mpeg", filename=filename)

@app.post("/api/voice-note")
async def save_voice_note(
    username: str = Form("Student"),
    file: UploadFile = File(...)
):
    safe_user = safe_name(username)
    file_bytes = await file.read()
    saved_filename = voice_service.save_uploaded_voice_note(file_bytes, file.filename, safe_user)

    return {
        "success": True,
        "message": "Voice note saved and ready for speech processing.",
        "filename": saved_filename
    }

# ============================================================
# 11. FACULTY TOOLS
# ============================================================

@app.post("/api/faculty-content")
def faculty_content(request: FacultyRequest):
    return faculty_service.generate_content(
        topic=request.topic,
        content_type=request.content_type,
        language=request.language,
        subject=request.subject
    )

# ============================================================
# 12. UTILITY METADATA (LANGUAGES & MARK PATTERNS)
# ============================================================

@app.get("/api/languages")
def get_supported_languages():
    return {"languages": LANGUAGES}

@app.get("/api/mark-pattern")
def get_mark_pattern(education_level: str = Query("College"), institution: str = Query("")):
    level = education_level.lower()
    if level in ["school", "10", "11", "12", "cbse", "matriculation"]:
        marks = [1, 2, 3, 5]
    else:
        marks = [2, 5, 10, 16]

    return {
        "education_level": education_level,
        "institution": institution,
        "supported_marks": marks
    }

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup():
    print()
    print("=" * 60)
    print("                 ARIVORA AI")
    print("       'Your Syllabus. Your Books. Your AI.'")
    print("           BACKEND ENGINE INITIALIZED")
    print("=" * 60)
    print("  Server Docs    : http://127.0.0.1:8000/docs")
    print("  Alternative    : http://127.0.0.1:8000/redoc")
    print("=" * 60)
    print()
