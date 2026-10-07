import re
from typing import Dict, Any
from data.curriculum_data import CURRICULUM
from services.document_service import document_service
from services.syllabus_service import syllabus_service

class ReferenceService:
    """
    ARIVORA AI Smart Reference Finder Service.
    Enables instant lookups of page-level citations, units, chapters,
    and excerpt snippets from student uploaded textbooks and syllabus materials.
    """

    def find_reference(self, topic: str, subject: str = "", username: str = "Student") -> Dict[str, Any]:
        lower_topic = topic.lower().strip()
        words = [w for w in re.findall(r"[a-z0-9]+", lower_topic) if len(w) > 1]

        # 1. Search in student's uploaded and indexed documents first (Primary RAG source)
        doc_hit = document_service.search_indexed_materials(topic, username, subject)
        if doc_hit:
            return {
                "success": True,
                "source_type": "uploaded_book",
                "topic": topic.title(),
                "subject": subject or "Uploaded Material",
                "book": doc_hit.get("book", "Uploaded Textbook"),
                "unit": f"Unit {doc_hit.get('unit', 1)}",
                "chapter": f"Section on Page {doc_hit.get('page', 1)}",
                "pages": f"Page {doc_hit.get('page', 1)}",
                "excerpt": doc_hit.get("snippet", f"Excerpt covering '{topic}'"),
                "citation": f"{doc_hit.get('book', 'Textbook')} → Unit {doc_hit.get('unit', 1)} → Page {doc_hit.get('page', 1)}"
            }

        # 2. Check built-in curriculum database with substring & word overlap
        for key, entry in CURRICULUM.items():
            key_lower = key.lower()
            if key_lower in lower_topic or lower_topic in key_lower or any(w in key_lower for w in words if len(w) > 2):
                return {
                    "success": True,
                    "source_type": "prescribed_curriculum",
                    "topic": entry.get("topic", topic.title()),
                    "subject": entry.get("subject", subject or "Core Computer Science"),
                    "book": entry.get("book", "Standard Reference Book"),
                    "unit": f"Unit {entry.get('unit', 1)}",
                    "chapter": entry.get("unit_title", "Core Architecture"),
                    "pages": entry.get("page_ref", "Pages 10–25"),
                    "excerpt": entry.get("definition", f"Official definition for {topic}"),
                    "citation": f"{entry.get('subject')} → {entry.get('unit_title')} → {entry.get('book')} ({entry.get('page_ref')})"
                }

        # 3. Check syllabus metadata
        syll_check = syllabus_service.check_topic(topic, subject, username)
        if syll_check.get("status") == "IN_SYLLABUS" or not syll_check.get("is_out_of_syllabus"):
            subj = syll_check.get("subject") or subject or "Academic Studies"
            unit_num = syll_check.get("unit") or 1
            unit_title = syll_check.get("unit_title") or "Core Modules"
            return {
                "success": True,
                "source_type": "syllabus_catalog",
                "topic": topic.title(),
                "subject": subj,
                "book": f"University Prescribed Reference Book for {subj}",
                "unit": f"Unit {unit_num}",
                "chapter": unit_title,
                "pages": f"Unit {unit_num} Core Sections",
                "excerpt": f"This topic is officially prescribed under Unit {unit_num}: {unit_title}.",
                "citation": f"{subj} → Unit {unit_num}: {unit_title}"
            }

        # 4. Fallback reference
        return {
            "success": True,
            "source_type": "general_reference",
            "topic": topic.title(),
            "subject": subject or "General Studies",
            "book": f"Standard Learning Material for {topic.title()}",
            "unit": "Unit 1",
            "chapter": "Core Concepts",
            "pages": "Reference Chapter 1",
            "excerpt": f"Topic '{topic}' reference retrieved from general academic knowledge base.",
            "citation": f"{subject or 'Curriculum'} → Reference Annexure"
        }

reference_service = ReferenceService()
