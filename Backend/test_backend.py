import os
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Ensure utf-8 printing on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_all_tests():
    print("=" * 70)
    print("         ARIVORA AI BACKEND - AUTOMATED VERIFICATION SUITE")
    print("=" * 70)

    # 1. Health & Root
    print("\n[TEST 1] Root & Health Check...")
    r = client.get("/", headers={"accept": "application/json"})
    assert r.status_code == 200, f"Root failed: {r.text}"
    data = r.json()
    assert data["project"] == "ARIVORA AI"
    print("  -> Root OK:", data["project"], "| Version:", data["version"])

    r = client.get("/health")
    assert r.status_code == 200
    print("  -> Health OK:", r.json()["status"])

    # 2. Academic Profile Creation
    print("\n[TEST 2] Profile Creation...")
    profile_payload = {
        "name": "Sameera",
        "role": "student",
        "board": "Anna University",
        "institution": "Engineering College",
        "medium": "English",
        "course": "B.E",
        "branch": "CSE",
        "languages": ["English", "Tamil"]
    }
    r = client.post("/api/profile", json=profile_payload)
    assert r.status_code == 200, f"Profile failed: {r.text}"
    p_data = r.json()
    assert p_data["success"] is True
    print("  -> Profile OK for user:", p_data["user"]["name"])

    # 3. 2-Mark Exam Answer with Tamil Support
    print("\n[TEST 3] 2-Mark Exam Answer (OSI Layers in Tamil)...")
    ans_payload = {
        "topic": "OSI layers",
        "marks": 2,
        "language": "Tamil",
        "subject": "Computer Networks",
        "username": "Sameera"
    }
    r = client.post("/api/answer", json=ans_payload)
    assert r.status_code == 200, f"Answer failed: {r.text}"
    a_data = r.json()
    assert a_data["marks"] == 2
    assert a_data["unit"] == 1
    assert "தமிழ் விளக்கம்" in a_data["answer"]
    print("  -> 2-Mark Answer OK:")
    print("     Subject :", a_data["subject"])
    print("     Unit    :", f"Unit {a_data['unit']}: {a_data['unit_title']}")
    print("     Ref     :", a_data["reference"])

    # 4. 16-Mark Comprehensive Essay Answer
    print("\n[TEST 4] 16-Mark University Essay (ACID Properties)...")
    ans_16_payload = {
        "topic": "ACID properties",
        "marks": 16,
        "language": "English",
        "subject": "DBMS",
        "username": "Sameera"
    }
    r = client.post("/api/answer", json=ans_16_payload)
    assert r.status_code == 200
    a16_data = r.json()
    assert a16_data["marks"] == 16
    assert "PART 1: INTRODUCTION" in a16_data["answer"]
    assert "PART 2: DETAILED ARCHITECTURAL BLOCK DIAGRAM" in a16_data["answer"]
    print("  -> 16-Mark Answer OK:")
    print("     Subject :", a16_data["subject"])
    print("     Unit    :", f"Unit {a16_data['unit']}: {a16_data['unit_title']}")
    print("     Length  :", len(a16_data["answer"]), "characters")

    # 5. Smart Reference Finder (Page-level citation)
    print("\n[TEST 5] Smart Reference Finder...")
    ref_payload = {
        "topic": "Normalization",
        "subject": "DBMS",
        "username": "Sameera"
    }
    r = client.post("/api/reference", json=ref_payload)
    assert r.status_code == 200
    ref_data = r.json()
    assert ref_data["success"] is True
    print("  -> Smart Reference OK:")
    print("     Citation:", ref_data["citation"])
    print("     Pages   :", ref_data["pages"])

    # 6. Syllabus Guardian (In-Syllabus vs Out-of-Syllabus)
    print("\n[TEST 6] Syllabus Guardian...")
    # In-syllabus
    r_in = client.get("/api/check-syllabus?topic=tcp/ip&subject=Computer Networks")
    assert r_in.status_code == 200
    in_data = r_in.json()
    assert in_data["status"] == "IN_SYLLABUS"
    print("  -> In-Syllabus Check OK:", in_data["message"])

    # Out-of-syllabus
    r_out = client.get("/api/check-syllabus?topic=Quantum Rocket Propulsion&subject=Computer Networks")
    assert r_out.status_code == 200
    out_data = r_out.json()
    assert out_data["status"] == "OUT_OF_SYLLABUS"
    print("  -> Out-of-Syllabus Check OK:", out_data["message"])
    print("     Suggestions:", out_data["recommended_in_syllabus_topics"][:2])

    # 7. Adaptive Quiz & Evaluation
    print("\n[TEST 7] Adaptive Quiz & Evaluation...")
    quiz_payload = {
        "topic": "OSI layers",
        "subject": "Computer Networks",
        "number_of_questions": 3,
        "language": "English"
    }
    r_q = client.post("/api/quiz", json=quiz_payload)
    assert r_q.status_code == 200
    q_data = r_q.json()
    assert len(q_data["questions"]) >= 3
    print("  -> Quiz Generation OK:", len(q_data["questions"]), "questions created.")

    # Evaluate
    eval_payload = {
        "topic": "OSI layers",
        "subject": "Computer Networks",
        "answers": {1: "B) Transport Layer", 2: "B) Data Link Layer"},
        "username": "Sameera"
    }
    r_ev = client.post("/api/quiz/evaluate", json=eval_payload)
    assert r_ev.status_code == 200
    ev_data = r_ev.json()
    assert "percentage" in ev_data
    print("  -> Quiz Evaluation OK | Score:", f"{ev_data['percentage']}%", "| Badge:", ev_data["badge"])

    # 8. Previous Year Questions (PYQ)
    print("\n[TEST 8] Previous Year Questions (Anna University)...")
    r_pyq = client.get("/api/previous-year-questions?university=Anna University&subject=Computer Networks")
    assert r_pyq.status_code == 200
    pyq_data = r_pyq.json()
    assert pyq_data["total_found"] > 0
    print("  -> PYQ Retrieval OK:", pyq_data["total_found"], "questions found.")
    print("     Sample Q:", pyq_data["questions"][0]["question"][:65] + "...")

    # 9. Voice AI (TTS speech generation)
    print("\n[TEST 9] Voice AI Speech Synthesis (gTTS)...")
    voice_payload = {
        "text": "Welcome to ARIVORA AI. Your Syllabus, Your Books, Your AI.",
        "language": "en",
        "username": "Sameera"
    }
    r_v = client.post("/api/voice-reply", json=voice_payload)
    assert r_v.status_code == 200
    v_data = r_v.json()
    assert v_data["success"] is True
    assert v_data["audio_url"] is not None
    print("  -> Voice TTS OK | Generated File:", v_data["filename"])

    # 10. Faculty AI Tools
    print("\n[TEST 10] Faculty AI Tools (Seminar Blueprint)...")
    fac_payload = {
        "topic": "OSI layers",
        "content_type": "seminar",
        "language": "English",
        "subject": "Computer Networks"
    }
    r_fac = client.post("/api/faculty-content", json=fac_payload)
    assert r_fac.status_code == 200
    fac_data = r_fac.json()
    assert "SLIDE 1: TITLE SLIDE" in fac_data["content"]
    print("  -> Faculty Tool OK:", fac_data["content_type"], "generated.")

    # 11. Revision Flashcards
    print("\n[TEST 11] Revision Flashcards...")
    r_rev = client.get("/api/revision-cards?topic=OSI layers")
    assert r_rev.status_code == 200
    rev_data = r_rev.json()
    assert len(rev_data["cards"]) > 0
    print("  -> Revision Cards OK:", len(rev_data["cards"]), "cards generated.")

    print("\n" + "=" * 70)
    print("🎉 ALL 11 TESTS COMPLETED SUCCESSFULLY! ARIVORA AI BACKEND IS PRODUCTION-READY.")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
