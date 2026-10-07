import os
import sys
import shutil
import json
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from services.document_service import document_service
from services.syllabus_service import syllabus_service
from services.ai_engine import ai_engine
from services.pyq_service import pyq_service
from config import STUDENT_DIR, INDEX_DIR

print("==================================================")
print("RUNNING AUTOMATED VERIFICATION FOR SCHOOL MODE FIXES")
print("==================================================")

username = "TestSchoolStudent"
role = "student"
user_base = STUDENT_DIR / username
user_base.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# TEST 1: Mathematics Folder & Document RAG
# --------------------------------------------------
math_folder = user_base / "Mathematics"
math_folder.mkdir(parents=True, exist_ok=True)

math_doc_path = math_folder / "Mathematics_Textbook.txt"
with open(math_doc_path, "w", encoding="utf-8") as f:
    f.write("""
    Chapter 1 - Fundamentals of Geometry
    Topic: Triangle Definitions and Properties
    Page 12: A triangle is a three-sided polygon with three vertices and three angles.
    Pythagoras theorem states that in a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides.
    a^2 + b^2 = c^2.
    """)

# Process text document
idx_res = document_service.process_text_file(math_doc_path, username, "Mathematics")
print("\n[TEST 1] Uploaded Math text indexing success:", idx_res is not None and len(idx_res.get("chunks", [])) > 0)

# Ask question in Mathematics folder
q1 = "What is the definition of a triangle?"
syll1 = syllabus_service.check_topic(q1, "Mathematics", username)
ans1 = ai_engine.generate_answer(q1, marks=5, language="English", subject="Mathematics", username=username)

print("[TEST 1] In-Syllabus check status:", syll1.get("status"))
print("[TEST 1] Is out of syllabus:", syll1.get("is_out_of_syllabus"))
print("[TEST 1] Book matched:", ans1.get("book") or syll1.get("book"))
print("[TEST 1] Chapter matched:", syll1.get("chapter"))
assert syll1.get("is_out_of_syllabus") == False, "Expected in-syllabus for Triangle in Mathematics folder"
assert "Mathematics_Textbook.txt" in (ans1.get("book") or syll1.get("book") or ""), "Expected book name to match uploaded file"

# --------------------------------------------------
# TEST 2: Out of Syllabus Detection inside Mathematics
# --------------------------------------------------
q2 = "Explain quantum computing."
syll2 = syllabus_service.check_topic(q2, "Mathematics", username)
ans2 = ai_engine.generate_answer(q2, marks=5, language="English", subject="Mathematics", username=username)

print("\n[TEST 2] Out of syllabus check status:", syll2.get("status"))
print("[TEST 2] Is out of syllabus:", syll2.get("is_out_of_syllabus"))
print("[TEST 2] Message:", ans2.get("message"))
print("[TEST 2] Allow General AI:", ans2.get("allow_general_ai"))
assert syll2.get("is_out_of_syllabus") == True, "Expected out_of_syllabus for quantum computing in Mathematics folder"
assert ans2.get("message") == "This topic is not available in your selected syllabus or uploaded learning materials.", "Message text mismatch"

# --------------------------------------------------
# TEST 3: Folder Isolation (Science vs Mathematics)
# --------------------------------------------------
sci_folder = user_base / "Science"
sci_folder.mkdir(parents=True, exist_ok=True)
sci_doc_path = sci_folder / "Science_Textbook.txt"
with open(sci_doc_path, "w", encoding="utf-8") as f:
    f.write("""
    Chapter 3 - Physics Principles
    Topic: Photosynthesis and Energy
    Page 45: Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water.
    """)

document_service.process_text_file(sci_doc_path, username, "Science")

# Ask Science question while in Mathematics folder
q3 = "What is photosynthesis?"
syll3_math = syllabus_service.check_topic(q3, "Mathematics", username)
print("\n[TEST 3] Photosynthesis in Math folder status:", syll3_math.get("status"))
print("[TEST 3] Photosynthesis in Math folder action:", syll3_math.get("action"))
print("[TEST 3] Suggested target folder:", syll3_math.get("folder_name"))
assert syll3_math.get("is_out_of_syllabus") == True, "Photosynthesis must be OUT OF SYLLABUS when inside Math folder"
assert syll3_math.get("folder_name") == "Science", "Should detect that Photosynthesis belongs to Science folder"

# Ask Science question while in Science folder
syll3_sci = syllabus_service.check_topic(q3, "Science", username)
print("[TEST 3] Photosynthesis in Science folder status:", syll3_sci.get("status"))
assert syll3_sci.get("is_out_of_syllabus") == False, "Photosynthesis must be IN SYLLABUS inside Science folder"

# --------------------------------------------------
# TEST 4: Previous Year Question Paper Live Web Search
# --------------------------------------------------
pyq_res = pyq_service.search_school_pyqs("Tamil Nadu State Board", "10", "Mathematics", 2025, "English")
print("\n[TEST 4] School PYQ Search success:", pyq_res.get("success"))
print("[TEST 4] Total papers found:", pyq_res.get("total_found"))
if pyq_res.get("questions"):
    print("[TEST 4] First paper title:", pyq_res["questions"][0]["title"])
    print("[TEST 4] First paper source:", pyq_res["questions"][0]["source"])
    print("[TEST 4] First paper URL:", pyq_res["questions"][0]["url"])

assert pyq_res.get("success") == True, "PYQ web search failed"
assert pyq_res.get("total_found") > 0, "No PYQ papers found"
assert pyq_res["questions"][0]["url"].startswith("http"), "PYQ paper URL is not a valid HTTP link"

# --------------------------------------------------
# TEST 5: Scanned PDF / Unreadable File Check
# --------------------------------------------------
empty_doc_path = math_folder / "Scanned_Image_Empty.txt"
with open(empty_doc_path, "w", encoding="utf-8") as f:
    f.write(" ") # Empty / unreadable text

empty_idx = document_service.process_text_file(empty_doc_path, username, "Mathematics")
print("\n[TEST 5] Unreadable/scanned doc check chars:", empty_idx.get("total_extracted_chars"))
assert empty_idx.get("total_extracted_chars") < 50, "Unreadable check failed"

print("\n==================================================")
print("ALL 5 TEST SCENARIOS PASSED SUCCESSFULLY! 🎉")
print("==================================================")
