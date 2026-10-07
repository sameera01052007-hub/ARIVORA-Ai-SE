from typing import Dict, Any
from data.curriculum_data import CURRICULUM
from services.ai_engine import ai_engine

class FacultyService:
    """
    ARIVORA AI Faculty & Educator Support Engine.
    Assists educators with seminar prep, lecture note synthesis,
    automated university question paper generation, and official answer keys.
    """

    def generate_content(self, topic: str, content_type: str = "seminar", language: str = "English", subject: str = "") -> Dict[str, Any]:
        c_type = content_type.lower().strip()
        unit_meta = ai_engine.detect_subject_and_unit(topic, subject)

        lower_topic = topic.lower().strip()
        entry = None
        for k, v in CURRICULUM.items():
            if k in lower_topic or lower_topic in k:
                entry = v
                break

        if c_type == "seminar":
            return self._build_seminar(topic, unit_meta, entry, language)
        elif c_type == "lecture":
            return self._build_lecture(topic, unit_meta, entry, language)
        elif c_type in ["questions", "question_paper"]:
            return self._build_question_paper(topic, unit_meta, entry, language)
        else:
            return self._build_answer_key(topic, unit_meta, entry, language)

    def _build_seminar(self, topic: str, meta: Dict, entry: Any, language: str) -> Dict[str, Any]:
        text = f"""
================================================================================
🎓 ARIVORA AI - FACULTY SEMINAR PRESENTATION BLUEPRINT
Subject : {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}
Topic   : {topic.title()}
Duration: 45 Minutes (35 mins lecture + 10 mins Q&A)
================================================================================

SLIDE 1: TITLE SLIDE
• Topic: {topic.title()}
• Target Course: {meta['subject']} ({meta['unit_title']})
• Instructor: Faculty Member

SLIDE 2: LEARNING OUTCOMES & PEDAGOGICAL OBJECTIVES
• By the end of this session, students will be able to:
  1. Formally define {topic.title()} and state its industrial necessity.
  2. Analyze the internal architectural layers and data flow.
  3. Solve 2-mark and 16-mark university examination questions.

SLIDE 3: CONCEPT OVERVIEW & TAXONOMY
• Academic Definition:
  {entry['definition'] if entry else f"Core foundational standard in {meta['subject']}."}

SLIDE 4: ARCHITECTURAL DIAGRAM & MECHANISM
{entry.get('architecture_diagram', '[Draw Block Diagram Here]') if entry else '[System Diagram]'}

SLIDE 5: REAL-WORLD INDUSTRIAL CASE STUDY
• Enterprise Deployment:
  {entry.get('applications', 'Widely adopted in scalable cloud architectures and networks.') if entry else 'Enterprise Case Study'}

SLIDE 6: CRITICAL THINKING / CLASSROOM DISCUSSION PROMPT
• "How does this architecture behave when network traffic increases tenfold?"

SLIDE 7: KEY TAKEAWAYS & EXAM POINTERS
• High-priority topic in university question papers.
• Emphasize drawing the neat flowchart and listing the ISO/IEEE specifications.
"""
        return {
            "success": True,
            "topic": topic,
            "content_type": "seminar",
            "subject": meta["subject"],
            "unit": meta["unit"],
            "content": text.strip()
        }

    def _build_lecture(self, topic: str, meta: Dict, entry: Any, language: str) -> Dict[str, Any]:
        text = f"""
================================================================================
📝 ARIVORA AI - COMPREHENSIVE LECTURE TEACHING NOTES
Course  : {meta['subject']} (Unit {meta['unit']} - {meta['unit_title']})
Topic   : {topic.title()}
Reference Book: {meta['book']} ({meta['page_ref']})
================================================================================

I. BLACKBOARD / SLIDE TEACHING STRUCTURE:
1. Warm-up Hook (3 mins): Introduce real-world problem solved by {topic.title()}.
2. Core Definition (7 mins): Deliver strict university standard definition.
3. Detailed Working (20 mins): Walk through component interactions step-by-step.
4. Numerical / Algorithmic Proof (10 mins).
5. Student Summary Check (5 mins).

II. DETAILED EXPLANATION NOTES FOR FACULTY:
{entry['definition'] if entry else 'Key concept definition.'}

Key Pillars:
"""
        if entry:
            for p in entry.get("key_points", []):
                text += f"• {p}\n"

        text += f"""
III. COMMON STUDENT MISCONCEPTIONS & CORRECTIONS:
• Misconception: Confusing logical design with physical hardware implementation.
• Clarification: Highlight the clear abstraction layer defined in {meta['unit_title']}.

IV. RECOMMENDED BOARD CITATION:
• Book: {meta['book']}
• Reading Assignment: {meta['page_ref']}
"""
        return {
            "success": True,
            "topic": topic,
            "content_type": "lecture",
            "subject": meta["subject"],
            "unit": meta["unit"],
            "content": text.strip()
        }

    def _build_question_paper(self, topic: str, meta: Dict, entry: Any, language: str) -> Dict[str, Any]:
        text = f"""
================================================================================
📋 ARIVORA AI - UNIVERSITY INTERNAL EXAMINATION QUESTION DRAFT
Subject : {meta['subject']} | Course Code: {meta.get('code', 'CS8001')}
Unit    : Unit {meta['unit']} - {meta['unit_title']}
================================================================================

PART A (Answer ALL Questions - 2 Marks Each)
--------------------------------------------------------------------------------
Q1. Define {topic.title()} and state its primary functional role in {meta['subject']}. (2 Marks)
Q2. State any two critical advantages of {topic.title()} in modern computing. (2 Marks)
Q3. What are the key performance metrics evaluated during the operation of {topic.title()}? (2 Marks)

PART B (Answer Either / Or - 16 Marks Each)
--------------------------------------------------------------------------------
Q4. (a) With a neat architectural diagram, explain the complete working principle,
        key components, and mathematical/protocol formulation of {topic.title()}. (16 Marks)
                                    (OR)
Q4. (b) (i) Conduct a comparative analysis between {topic.title()} and traditional approaches. (8 Marks)
        (ii) Discuss a real-world enterprise case study illustrating practical deployment. (8 Marks)
"""
        return {
            "success": True,
            "topic": topic,
            "content_type": "questions",
            "subject": meta["subject"],
            "unit": meta["unit"],
            "content": text.strip()
        }

    def _build_answer_key(self, topic: str, meta: Dict, entry: Any, language: str) -> Dict[str, Any]:
        text = f"""
================================================================================
🔑 ARIVORA AI - OFFICIAL FACULTY EVALUATION ANSWER KEY & RUBRIC
Subject : {meta['subject']} | Topic: {topic.title()}
================================================================================

PART A: 2-MARK EVALUATION SCHEME
• Criteria 1: Accurate Definition (1 Mark)
  Expected: {entry['definition'][:120] if entry else 'Accurate academic definition.'}
• Criteria 2: Two relevant features / formulas / examples (1 Mark)
  Expected: Clear bullet points directly referencing {meta['unit_title']}.

PART B: 16-MARK EVALUATION SCHEME
• Neat Labelled Architectural Diagram      : 4 Marks
• Explanation of Working Principle & Steps: 6 Marks
• Mathematical/Protocol Analysis          : 3 Marks
• Real-World Applications & Advantages    : 3 Marks
--------------------------------------------------------------------------------
TOTAL                                     : 16 Marks
"""
        return {
            "success": True,
            "topic": topic,
            "content_type": "answer_key",
            "subject": meta["subject"],
            "unit": meta["unit"],
            "content": text.strip()
        }

faculty_service = FacultyService()
