import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import pymupdf

from config import INDEX_DIR, SUBJECT_CATALOG, SUBJECT_ALIASES

# Try importing OCR components if installed
HAS_OCR = False
try:
    import pytesseract
    from PIL import Image
    import io
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

STOP_WORDS = {
    "explain", "what", "is", "are", "the", "in", "define", "about", "notes",
    "on", "give", "tell", "me", "concept", "concepts", "main", "please",
    "describe", "discuss", "types", "of", "and", "an", "a", "to", "for", "with",
    "at", "from", "by", "as", "into", "like", "through", "after", "over",
    "between", "out", "against", "during", "without", "before", "under", "around",
    "among", "detail", "details", "summary", "working", "overview", "show", "find"
}

class DocumentService:
    def __init__(self):
        self.index_dir = INDEX_DIR
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def _clean_text(self, text: str) -> str:
        """Removes extra whitespaces and control characters."""
        return re.sub(r"\s+", " ", text).strip()

    def _extract_core_terms(self, text: str) -> List[str]:
        words = [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", text) if w.lower() not in STOP_WORDS and len(w) > 1]
        return words

    def process_pdf(self, file_path: Path, username: str, subject: str) -> Dict[str, Any]:
        """
        Parses a PDF textbook or syllabus using PyMuPDF (with OCR fallback for scanned PDFs),
        extracts page text, identifies Units/Chapters/Topics, splits into semantic chunks with term vectors,
        and builds a searchable index preserving user_id, folder_id, and document_id metadata.
        """
        doc = pymupdf.open(str(file_path))
        total_pages = len(doc)
        pages_data = []
        chunks_data = []
        detected_units = []
        detected_topics = []

        unit_pattern = re.compile(
            r"(?:UNIT\s*[-–—:]*\s*([IVXLCDM\d]+)|CHAPTER\s*[-–—:]*\s*(\d+))\s*[-–—:]*\s*([A-Za-z0-9 ,&/'\-]+)?",
            re.IGNORECASE
        )
        topic_pattern = re.compile(
            r"^(?:[0-9]+\.[0-9]+\s+|TOPIC\s*:\s*)([A-Za-z0-9 ,&/\-]{3,60})",
            re.MULTILINE | re.IGNORECASE
        )

        current_unit = None
        total_extracted_chars = 0
        max_pages = min(total_pages, 150)

        for page_idx in range(max_pages):
            page_num = page_idx + 1
            page = doc[page_idx]
            text = page.get_text("text") or ""
            cleaned = self._clean_text(text)

            total_extracted_chars += len(cleaned)

            # Detect Unit / Chapter headers
            unit_match = unit_pattern.search(cleaned)
            if unit_match:
                unit_val = unit_match.group(1) or unit_match.group(2)
                unit_title = (unit_match.group(3) or "").strip()
                current_unit = {
                    "unit": unit_val,
                    "title": unit_title if unit_title else f"Chapter {unit_val}",
                    "page": page_num
                }
                detected_units.append(current_unit)

            # Detect specific section topics
            for tm in topic_pattern.finditer(cleaned):
                topic_title = tm.group(1).strip()
                if len(topic_title) > 3 and not any(t["topic"].lower() == topic_title.lower() for t in detected_topics):
                    detected_topics.append({
                        "topic": topic_title,
                        "page": page_num,
                        "unit": current_unit["unit"] if current_unit else 1
                    })

            chap_name = current_unit["title"] if current_unit else f"Chapter on Page {page_num}"
            unit_id = current_unit["unit"] if current_unit else 1

            pages_data.append({
                "page": page_num,
                "text": cleaned[:2000],
                "char_count": len(cleaned),
                "unit": unit_id,
                "chapter": chap_name
            })

            # Fast Semantic chunking (~250 words per chunk)
            if len(cleaned) > 50:
                words = cleaned.split()
                chunk_size = 200
                overlap = 30
                for i in range(0, len(words), chunk_size - overlap):
                    chunk_words = words[i:i + chunk_size]
                    if len(chunk_words) < 10:
                        continue
                    chunk_text = " ".join(chunk_words)
                    terms = self._extract_core_terms(chunk_text)
                    chunks_data.append({
                        "chunk_id": f"p{page_num}_c{i}",
                        "page": page_num,
                        "unit": unit_id,
                        "chapter": chap_name,
                        "text": chunk_text,
                        "terms": terms
                    })

        doc.close()

        is_scanned_unreadable = total_extracted_chars < 50

        index_record = {
            "filename": file_path.name,
            "document_id": file_path.name,
            "username": username,
            "user_id": username,
            "subject": subject,
            "folder_id": subject,
            "subject_clean": subject.replace("_", " "),
            "total_pages": total_pages,
            "total_extracted_chars": total_extracted_chars,
            "is_scanned": is_scanned_unreadable,
            "unreadable": is_scanned_unreadable,
            "units": detected_units,
            "topics": detected_topics[:50],
            "pages": pages_data,
            "chunks": chunks_data
        }

        # Save index to disk fast without indent formatting overhead
        safe_user = re.sub(r"[^a-zA-Z0-9_-]", "_", username)
        safe_subj = re.sub(r"[^a-zA-Z0-9_-]", "_", subject)
        safe_stem = re.sub(r"[^a-zA-Z0-9_-]", "_", file_path.stem)
        safe_base = f"{safe_user}_{safe_subj}_{safe_stem}"
        
        index_file = self.index_dir / f"{safe_base}.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index_record, f, ensure_ascii=False)

        return index_record

    def process_text_file(self, file_path: Path, username: str, subject: str) -> Dict[str, Any]:
        """Processes plain text or notes document."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            content = ""

        cleaned = self._clean_text(content)
        pages_data = [{
            "page": 1,
            "text": cleaned[:5000],
            "char_count": len(cleaned),
            "unit": 1,
            "chapter": "Notes / Document Material"
        }]

        words = cleaned.split()
        chunks_data = []
        if len(words) > 5:
            for i in range(0, len(words), 80):
                chunk_words = words[i:i + 100]
                chunk_text = " ".join(chunk_words)
                terms = self._extract_core_terms(chunk_text)
                chunks_data.append({
                    "chunk_id": f"c{i}",
                    "page": 1,
                    "unit": 1,
                    "chapter": "Notes / Document Material",
                    "text": chunk_text,
                    "terms": terms
                })

        index_record = {
            "filename": file_path.name,
            "document_id": file_path.name,
            "username": username,
            "user_id": username,
            "subject": subject,
            "folder_id": subject,
            "subject_clean": subject.replace("_", " "),
            "total_pages": 1,
            "total_extracted_chars": len(cleaned),
            "is_scanned": False,
            "unreadable": False,
            "units": [],
            "topics": [],
            "pages": pages_data,
            "chunks": chunks_data
        }

        safe_user = re.sub(r"[^a-zA-Z0-9_-]", "_", username)
        safe_subj = re.sub(r"[^a-zA-Z0-9_-]", "_", subject)
        safe_stem = re.sub(r"[^a-zA-Z0-9_-]", "_", file_path.stem)
        index_file = self.index_dir / f"{safe_user}_{safe_subj}_{safe_stem}.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index_record, f, ensure_ascii=False, indent=2)

        return index_record

    def search_indexed_materials(self, query: str, username: str, subject: str = "") -> Optional[Dict[str, Any]]:
        """
        Searches processed documents belonging STRICTLY to this user and active subject folder.
        Filters by user_id and folder_id to ensure complete folder isolation.
        Performs vector semantic scoring over document chunks.
        """
        core_query_terms = self._extract_core_terms(query)
        if not core_query_terms:
            return None

        clean_query = query.lower().strip()
        user_lower = (username or "").strip().lower()

        def norm_subj(s: str) -> str:
            return re.sub(r"[^a-z0-9]", "", (s or "").lower())

        target_norm = norm_subj(subject)

        best_match = None
        highest_score = 0.0

        for idx_path in self.index_dir.glob("*.json"):
            try:
                with open(idx_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # 1. Strict User Isolation
                doc_user = (data.get("username") or data.get("user_id") or "").strip().lower()
                if user_lower and doc_user and doc_user != user_lower:
                    continue

                # 2. Strict Folder Isolation
                if target_norm and target_norm not in ["general", "all", "generalai"]:
                    doc_subj_norm = norm_subj(data.get("subject_clean") or data.get("subject") or data.get("folder_id") or "")
                    if doc_subj_norm != target_norm:
                        continue

                # Search semantic chunks if available, else fall back to pages
                search_units = data.get("chunks") if data.get("chunks") else data.get("pages", [])

                for item in search_units:
                    item_text = (item.get("text") or "").lower()
                    if not item_text:
                        continue

                    # Vector / term overlap scoring
                    item_terms = item.get("terms") or self._extract_core_terms(item_text)
                    matched_core = [w for w in core_query_terms if w in item_terms or w in item_text]
                    coverage_ratio = len(matched_core) / len(core_query_terms) if core_query_terms else 0.0

                    # Check multi-word phrase match
                    phrase_match = clean_query in item_text or any(
                        " ".join(core_query_terms[i:i+2]) in item_text
                        for i in range(len(core_query_terms)-1)
                    ) if len(core_query_terms) > 1 else False

                    # Threshold requirement: coverage >= 0.50 or exact phrase match
                    if coverage_ratio < 0.50 and not phrase_match:
                        continue

                    score = (coverage_ratio * 10) + (5.0 if phrase_match else 0.0)

                    if score > highest_score:
                        highest_score = score

                        # Snippet extraction around best keyword match
                        first_word = next((w for w in matched_core if w in item_text), core_query_terms[0])
                        pos = item_text.find(first_word)
                        start = max(0, pos - 80)
                        end = min(len(item.get("text", "")), pos + 300)
                        snippet = "..." + item.get("text", "")[start:end] + "..."

                        best_match = {
                            "book": data.get("filename"),
                            "filename": data.get("filename"),
                            "document_id": data.get("document_id") or data.get("filename"),
                            "user_id": data.get("username"),
                            "folder_id": data.get("subject"),
                            "page": item.get("page", 1),
                            "unit": item.get("unit", 1),
                            "chapter": item.get("chapter") or f"Chapter {item.get('unit', 1)}",
                            "topic": query.title(),
                            "score": score,
                            "coverage_ratio": coverage_ratio,
                            "snippet": snippet or item.get("text", "")[:250]
                        }
            except Exception:
                continue

        return best_match if highest_score >= 4.5 else None

document_service = DocumentService()

