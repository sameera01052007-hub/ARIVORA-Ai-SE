import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent))

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from main import app

client = TestClient(app)

def test_school_folder_features():
    print("=" * 60)
    print("      TESTING SCHOOL VS COLLEGE FOLDER SYSTEM & ISOLATION")
    print("=" * 60)

    # 1. College Student Test
    print("\n[TEST 1] College Student Profile & Folders...")
    college_profile = {
        "name": "CollegeUserTest",
        "role": "student",
        "education": "College",
        "board": "Anna University"
    }
    r = client.post("/api/profile", json=college_profile)
    assert r.status_code == 200

    r_folders = client.get("/api/folders?username=CollegeUserTest&role=student&education=College")
    assert r_folders.status_code == 200
    c_folders = [f["name"] for f in r_folders.json()["folders"]]
    print("  -> College Student Folders Count:", len(c_folders))
    assert "Computer Networks" in c_folders
    assert "DBMS" in c_folders
    print("  ✓ College Student sees predefined catalog folders.")

    # Clean up any leftover test folder for SchoolStudentA
    import shutil
    s_dir = os.path.join(UPLOAD_DIR, "students", "SchoolStudentA")
    if os.path.exists(s_dir):
        shutil.rmtree(s_dir)

    # 2. School Student Test - Empty Initial State
    print("\n[TEST 2] School Student Initial State...")
    school_profile = {
        "name": "SchoolStudentA",
        "role": "student",
        "education": "School",
        "board": "Tamil Nadu State Board"
    }
    r = client.post("/api/profile", json=school_profile)
    assert r.status_code == 200

    r_school_folders = client.get("/api/folders?username=SchoolStudentA&role=student&education=School")
    assert r_school_folders.status_code == 200
    s_folders = r_school_folders.json()["folders"]
    print("  -> School Student Initial Folders Count:", len(s_folders))
    assert len(s_folders) == 0, f"School student should start with 0 folders, got {s_folders}"
    print("  ✓ School Student starts with empty folders (no predefined college folders).")

    # 3. Custom Folder Creation for School Student A
    print("\n[TEST 3] Custom Folder Creation for School Student A...")
    folders_to_create = ["Mathematics", "Science", "Social Science"]
    for fname in folders_to_create:
        cf_req = {
            "folder_name": fname,
            "username": "SchoolStudentA",
            "role": "student"
        }
        res = client.post("/api/create-folder", json=cf_req)
        assert res.status_code == 200
        assert res.json()["success"] is True

    r_updated = client.get("/api/folders?username=SchoolStudentA&role=student&education=School")
    assert r_updated.status_code == 200
    a_folder_names = [f["name"] for f in r_updated.json()["folders"]]
    print("  -> School Student A Folders:", a_folder_names)
    assert "Mathematics" in a_folder_names
    assert "Science" in a_folder_names
    assert "Social Science" in a_folder_names
    assert "Computer Networks" not in a_folder_names
    print("  ✓ Custom folders created and listed successfully.")

    # 4. User Isolation Test (School Student B)
    print("\n[TEST 4] User Isolation (School Student B)...")
    student_b_profile = {
        "name": "SchoolStudentB",
        "role": "student",
        "education": "School",
        "board": "CBSE"
    }
    client.post("/api/profile", json=student_b_profile)

    # Create folder for Student B
    client.post("/api/create-folder", json={"folder_name": "Physics", "username": "SchoolStudentB", "role": "student"})

    r_b = client.get("/api/folders?username=SchoolStudentB&role=student&education=School")
    b_folder_names = [f["name"] for f in r_b.json()["folders"]]
    print("  -> School Student B Folders:", b_folder_names)
    assert "Physics" in b_folder_names
    assert "Mathematics" not in b_folder_names
    assert "Science" not in b_folder_names
    print("  ✓ Student B does NOT see Student A's folders (User Isolation verified).")

    print("\n" + "=" * 60)
    print("  🎉 ALL SCHOOL FOLDER SYSTEM TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_school_folder_features()
