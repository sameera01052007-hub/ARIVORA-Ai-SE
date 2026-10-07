import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Ensure utf-8 printing on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from main import app

client = TestClient(app)

def test_system():
    print("=" * 60)
    print("      ARIVORA AI - FULL SYSTEM & ENDPOINT VERIFICATION")
    print("=" * 60)

    # 1. Static Frontend App Mount
    r = client.get("/app/")
    assert r.status_code == 200
    assert "<title>ARIVORA AI" in r.text
    print("  ✓ /app/ static HTML served successfully.")

    # 2. API Health
    r = client.get("/health")
    assert r.status_code == 200
    print("  ✓ /health endpoint active.")

    # 3. User Profile Creation & Retrieval
    prof = {
        "name": "Sameera",
        "role": "student",
        "board": "Anna University",
        "institution": "Engineering College",
        "medium": "English",
        "course": "B.E",
        "branch": "CSE",
        "languages": ["English", "Tamil"]
    }
    r = client.post("/api/profile", json=prof)
    assert r.status_code == 200
    print("  ✓ /api/profile endpoint OK.")

    # 4. Folders listing
    r = client.get("/api/folders?username=Sameera&role=student")
    assert r.status_code == 200
    assert "folders" in r.json()
    print("  ✓ /api/folders listing OK.")

    # 5. Dynamic Exam Answer (2-Mark, 5-Mark, 16-Mark)
    for marks in [2, 5, 16]:
        ans = client.post("/api/answer", json={
            "topic": "OSI layers",
            "marks": marks,
            "language": "English",
            "subject": "Computer Networks",
            "username": "Sameera"
        })
        assert ans.status_code == 200
        data = ans.json()
        assert data["marks"] == marks
        print(f"  ✓ /api/answer ({marks}-mark essay/definition) OK.")

    # 6. Syllabus Check Endpoint
    chk = client.get("/api/check-syllabus?topic=tcp/ip&subject=Computer Networks")
    assert chk.status_code == 200
    assert chk.json()["status"] in ["supported", "IN_SYLLABUS"]
    print("  ✓ /api/check-syllabus (Syllabus Guardian) OK.")

    # 7. Reference Finder Endpoint
    ref = client.post("/api/reference", json={"topic": "Normalization", "subject": "DBMS"})
    assert ref.status_code == 200
    assert ref.json()["success"] is True
    print("  ✓ /api/reference (Smart Reference Finder) OK.")

    # 8. Quiz & Evaluation
    qz = client.post("/api/quiz", json={"topic": "OSI layers", "subject": "Computer Networks", "number_of_questions": 3})
    assert qz.status_code == 200
    print("  ✓ /api/quiz generation OK.")

    ev = client.post("/api/quiz/evaluate", json={"topic": "OSI layers", "subject": "Computer Networks", "answers": {1: "B) Transport Layer"}})
    assert ev.status_code == 200
    print("  ✓ /api/quiz/evaluate evaluation OK.")

    # 9. Revision Cards
    rev = client.get("/api/revision-cards?topic=OSI layers")
    assert rev.status_code == 200
    print("  ✓ /api/revision-cards OK.")

    # 10. Previous Year Questions (PYQ)
    pyq = client.get("/api/previous-year-questions?university=Anna University&subject=Computer Networks")
    assert pyq.status_code == 200
    print("  ✓ /api/previous-year-questions OK.")

    # 11. Timetable & Today's Study Plan
    tt = client.get("/api/timetable?username=Sameera")
    assert tt.status_code == 200
    assert "today_plan" in tt.json()
    print("  ✓ /api/timetable & study planner OK.")

    # 12. Voice TTS
    v = client.post("/api/voice-reply", json={"text": "Hello ARIVORA", "language": "en"})
    assert v.status_code == 200
    print("  ✓ /api/voice-reply OK.")

    # 13. Faculty Content Blueprint
    fac = client.post("/api/faculty-content", json={"topic": "OSI layers", "content_type": "seminar", "language": "English", "subject": "Computer Networks"})
    assert fac.status_code == 200
    print("  ✓ /api/faculty-content OK.")

    # 14. Metadata Languages & Mark Patterns
    lang = client.get("/api/languages")
    assert lang.status_code == 200
    print("  ✓ /api/languages OK.")

    mp = client.get("/api/mark-pattern?education_level=College")
    assert mp.status_code == 200
    assert mp.json()["supported_marks"] == [2, 5, 10, 16]
    print("  ✓ /api/mark-pattern OK.")

    print("\n" + "=" * 60)
    print("  🎉 ALL 14 SYSTEM TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_system()
