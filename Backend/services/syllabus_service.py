import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from config import SUBJECT_CATALOG, SUBJECT_ALIASES, STUDENT_DIR, FACULTY_DIR, INDEX_DIR
from data.curriculum_data import CURRICULUM
from services.document_service import document_service

class SyllabusService:
    """
    Syllabus Guardian Service:
    Validates queries and learning materials against prescribed syllabus boundaries.
    Intelligently checks if an out-of-syllabus topic exists in the user's uploaded folders/materials:
    - If user has a folder/document: Prompts 'Out of the syllabus. Go and refer [Folder Name]'
    - If user has NOT uploaded anything for this topic: Prompts 'Out of the syllabus. Left out of the syllabus. Go and ask General AI'
    """

    def normalize_subject(self, subject_str: str) -> Optional[str]:
        if not subject_str:
            return None
        s = subject_str.lower().strip().replace("_", " ")
        if s in ["general", "all", "general ai"]:
            return "general"
        if s in SUBJECT_ALIASES:
            return SUBJECT_ALIASES[s]
        for k, v in SUBJECT_CATALOG.items():
            if k in s or s in k or v["name"].lower() == s:
                return k
        return None

    def _extract_keywords(self, text: str) -> List[str]:
        lt = text.lower().strip()
        stop_words = {
            "explain", "what", "is", "are", "the", "in", "define", "about",
            "notes", "on", "give", "tell", "me", "concept", "concepts", "main",
            "please", "describe", "discuss", "types", "of", "and", "an", "a",
            "tamil", "thanglish", "tanglish", "english", "la", "kaamikkanum",
            "details", "summary", "working", "overview"
        }
        words = [w for w in re.findall(r"[a-z0-9]+", lt) if w not in stop_words and len(w) > 1]
        return words

    def _find_topic_in_subject(self, topic: str, sub_key: str) -> Optional[Dict[str, Any]]:
        lt = topic.lower().strip()
        words = self._extract_keywords(topic)
        cleaned = " ".join(words)

        # 1. CURRICULUM check
        for c_key, c_val in CURRICULUM.items():
            c_sub = self.normalize_subject(c_val["subject"])
            if c_sub == sub_key:
                if c_key in lt or lt in c_key or (cleaned and (c_key in cleaned or cleaned in c_key)):
                    return {
                        "unit": c_val["unit"],
                        "unit_title": c_val["unit_title"],
                        "topic_title": c_val.get("topic", c_key.title()),
                        "book": c_val.get("book", "")
                    }
                c_words = set(re.findall(r"[a-z0-9]+", c_key))
                if any(w in c_words for w in words if len(w) > 2):
                    return {
                        "unit": c_val["unit"],
                        "unit_title": c_val["unit_title"],
                        "topic_title": c_val.get("topic", c_key.title()),
                        "book": c_val.get("book", "")
                    }

        # 2. SUBJECT_CATALOG check
        cat = SUBJECT_CATALOG.get(sub_key)
        if not cat:
            return None

        for u in cat["units"]:
            for t in u["topics"]:
                if t in lt or lt in t or (cleaned and (t in cleaned or cleaned in t)):
                    return {
                        "unit": u["unit"],
                        "unit_title": u["title"],
                        "topic_title": t.title(),
                        "book": f"Standard Textbook for {cat['name']}"
                    }
                t_words = set(re.findall(r"[a-z0-9]+", t))
                overlap = t_words.intersection(words)
                if len(overlap) >= 2 or (len(overlap) == 1 and any(len(w) >= 4 for w in overlap if w not in {"data", "model", "system", "layer", "level"})):
                    return {
                        "unit": u["unit"],
                        "unit_title": u["title"],
                        "topic_title": t.title(),
                        "book": f"Standard Textbook for {cat['name']}"
                    }

        return None

    def _find_matching_user_or_catalog_folder(self, topic: str, username: str = "Student") -> Optional[Dict[str, Any]]:
        """
        Scans:
        1. User's indexed materials across ALL uploaded folders (document_service)
        2. User's physical uploaded folders & files (STUDENT_DIR / safe_name)
        3. Other standard subject catalog folders
        Returns details of the matching folder if found.
        """
        lt = topic.lower().strip()
        words = self._extract_keywords(topic)

        # A. Check all user's indexed materials across folders
        any_doc_match = document_service.search_indexed_materials(topic, username, subject="")
        if any_doc_match:
            fn = any_doc_match.get("folder_id") or any_doc_match.get("subject") or "General"
            return {
                "folder_name": fn.replace("_", " "),
                "folder_key": fn,
                "source": "indexed_material",
                "filename": any_doc_match.get("filename")
            }

        # B. User uploaded folders & files name check
        safe_user = re.sub(r"[^a-zA-Z0-9._-]", "_", username or "Student")[:100]
        user_base = STUDENT_DIR / safe_user
        if user_base.exists():
            for folder_dir in user_base.iterdir():
                if folder_dir.is_dir():
                    clean_folder_name = folder_dir.name.replace("_", " ").lower()
                    if any(w in clean_folder_name for w in words if len(w) > 2) or clean_folder_name in lt or lt in clean_folder_name:
                        return {
                            "folder_name": folder_dir.name.replace("_", " "),
                            "folder_key": folder_dir.name,
                            "source": "user_folder"
                        }
                    for file in folder_dir.iterdir():
                        if file.is_file():
                            fn_clean = file.stem.lower().replace("_", " ")
                            if any(w in fn_clean for w in words if len(w) > 2) or fn_clean in lt or lt in fn_clean:
                                return {
                                    "folder_name": folder_dir.name.replace("_", " "),
                                    "folder_key": folder_dir.name,
                                    "source": "user_file",
                                    "filename": file.name
                                }

        # C. Check other subject folders in catalog
        for cat_key, cat_val in SUBJECT_CATALOG.items():
            match = self._find_topic_in_subject(topic, cat_key)
            if match:
                return {
                    "folder_name": cat_val["name"],
                    "folder_key": cat_val["folder"],
                    "source": "catalog_folder",
                    "unit": match["unit"],
                    "unit_title": match["unit_title"]
                }

        return None

    def check_topic(self, topic: str, subject: str = "", username: str = "Student") -> Dict[str, Any]:
        """
        Validates topic against active syllabus / folder using document RAG search.
        If user is inside a selected custom folder:
        - Checks whether topic exists in that folder's uploaded materials or prescribed catalog.
        - If NOT found: returns structured OUT_OF_SYLLABUS response.
        """
        if not topic or not topic.strip():
            return {
                "status": "supported",
                "is_out_of_syllabus": False,
                "message": "Valid topic required"
            }

        clean_subject = (subject or "").strip()
        curr_key = self.normalize_subject(clean_subject)
        subject_display_name = clean_subject.replace("_", " ") if clean_subject else "General"

        # 1. Check if topic exists in user's uploaded documents for active subject folder (Primary RAG source)
        if clean_subject and clean_subject.lower() not in ["general", "all", "general ai"]:
            doc_match = document_service.search_indexed_materials(topic, username, clean_subject)
            if doc_match:
                return {
                    "status": "supported",
                    "is_out_of_syllabus": False,
                    "topic": topic,
                    "subject": subject_display_name,
                    "folder": clean_subject,
                    "unit": doc_match.get("unit", 1),
                    "unit_title": doc_match.get("chapter") or f"Page {doc_match.get('page', 1)} Material",
                    "book": doc_match.get("book", "Uploaded Material"),
                    "chapter": doc_match.get("chapter"),
                    "page": doc_match.get("page"),
                    "snippet": doc_match.get("snippet"),
                    "confidence": doc_match.get("coverage_ratio", 0.90),
                    "message": f"Uploaded Material Verified: '{topic}' found in {doc_match.get('book', 'uploaded file')} ({subject_display_name})."
                }

        # 2. Check if topic exists in active subject catalog (College fallback)
        if curr_key and curr_key != "general" and curr_key in SUBJECT_CATALOG:
            curr_cat = SUBJECT_CATALOG[curr_key]
            subject_display_name = curr_cat["name"]
            this_match = self._find_topic_in_subject(topic, curr_key)
            if this_match:
                return {
                    "status": "supported",
                    "is_out_of_syllabus": False,
                    "topic": topic,
                    "subject": subject_display_name,
                    "folder": curr_cat["folder"],
                    "unit": this_match["unit"],
                    "unit_title": this_match["unit_title"],
                    "confidence": 0.95,
                    "message": f"In-Syllabus Verified: '{topic}' is part of Unit {this_match['unit']} ({this_match['unit_title']}) in {subject_display_name}."
                }

        # -------------------------------------------------------------
        # IF ACTIVE SUBJECT / FOLDER IS SPECIFIED AND TOPIC IS NOT IN IT:
        # IT IS OUT OF SYLLABUS FOR THIS FOLDER!
        # -------------------------------------------------------------
        if clean_subject and clean_subject.lower() not in ["general", "all", "general ai"]:
            # Find if another folder uploaded by user contains this topic
            matched_folder = self._find_matching_user_or_catalog_folder(topic, username)
            
            if matched_folder and matched_folder["folder_name"].lower().replace("_", " ") != subject_display_name.lower().replace("_", " "):
                fn = matched_folder["folder_name"]
                fk = matched_folder.get("folder_key", fn.replace(" ", "_"))
                return {
                    "status": "out_of_syllabus",
                    "is_out_of_syllabus": True,
                    "topic": topic,
                    "current_subject": subject_display_name,
                    "current_folder": clean_subject,
                    "belongs_to_folder": True,
                    "action": "REFER_FOLDER",
                    "folder_name": fn,
                    "folder_key": fk,
                    "message": "This topic is not available in your selected syllabus or uploaded learning materials.",
                    "advice": f"This topic belongs to your '{fn}' folder. Switch to '{fn}' folder or ask General AI.",
                    "recommended_in_syllabus_topics": self._find_nearest_topics(topic, curr_key)
                }

            # Topic is not in current folder AND user has no folder for it anywhere
            return {
                "status": "out_of_syllabus",
                "is_out_of_syllabus": True,
                "topic": topic,
                "current_subject": subject_display_name,
                "current_folder": clean_subject,
                "belongs_to_folder": False,
                "action": "ASK_GENERAL_AI",
                "folder_name": None,
                "folder_key": None,
                "message": "This topic is not available in your selected syllabus or uploaded learning materials.",
                "advice": "This topic is not available in your uploaded materials. You can ask General AI.",
                "recommended_in_syllabus_topics": self._find_nearest_topics(topic, curr_key)
            }

        # -------------------------------------------------------------
        # SCENARIO B: Subject is General or empty
        # -------------------------------------------------------------
        for cat_key, cat_val in SUBJECT_CATALOG.items():
            match = self._find_topic_in_subject(topic, cat_key)
            if match:
                return {
                    "status": "IN_SYLLABUS",
                    "is_out_of_syllabus": False,
                    "topic": topic,
                    "subject": cat_val["name"],
                    "folder": cat_val["folder"],
                    "unit": match["unit"],
                    "unit_title": match["unit_title"],
                    "confidence": 0.90,
                    "message": f"✅ Verified: '{topic}' matches Unit {match['unit']} ({match['unit_title']}) in {cat_val['name']}."
                }

        # Check if user has an uploaded folder
        matched_folder = self._find_matching_user_or_catalog_folder(topic, username)
        if matched_folder:
            fn = matched_folder["folder_name"]
            fk = matched_folder.get("folder_key", fn.replace(" ", "_"))
            return {
                "status": "OUT_OF_SYLLABUS",
                "is_out_of_syllabus": True,
                "topic": topic,
                "belongs_to_folder": True,
                "action": "REFER_FOLDER",
                "folder_name": fn,
                "folder_key": fk,
                "message": f"Out of the syllabus. Go and refer to your '{fn}' folder.",
                "advice": f"Out of the syllabus. You have a folder for this: '{fn}'. Go and refer.",
                "recommended_in_syllabus_topics": self._find_nearest_topics(topic)
            }

        # Completely unuploaded topic
        return {
            "status": "OUT_OF_SYLLABUS",
            "is_out_of_syllabus": True,
            "topic": topic,
            "belongs_to_folder": False,
            "action": "ASK_GENERAL_AI",
            "folder_name": None,
            "folder_key": None,
            "message": "Out of the syllabus. Left out of the syllabus. Go and ask General AI.",
            "advice": "Out of the syllabus. You haven't uploaded any materials for this topic. Go and ask General AI.",
            "recommended_in_syllabus_topics": self._find_nearest_topics(topic)
        }

    def _find_nearest_topics(self, query: str, subject_key: str = None) -> List[str]:
        suggestions = []
        target_catalogs = [SUBJECT_CATALOG[subject_key]] if subject_key and subject_key in SUBJECT_CATALOG else list(SUBJECT_CATALOG.values())
        for cat in target_catalogs:
            for u in cat.get("units", []):
                for t in u.get("topics", []):
                    suggestions.append(f"{t.title()} ({cat['name']} - Unit {u['unit']})")
                    if len(suggestions) >= 4:
                        return suggestions
        return suggestions[:4]

syllabus_service = SyllabusService()
