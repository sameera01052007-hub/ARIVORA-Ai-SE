import re
from typing import Dict, Any, Optional
from config import SUBJECT_CATALOG, SUBJECT_ALIASES, OPENAI_API_KEY
from data.curriculum_data import CURRICULUM
from services.document_service import document_service
import openai

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

class AIEngine:
    """
    ARIVORA AI Exam-Oriented Academic Answer Synthesis Engine.
    Generates tailored 2, 5, 10, and 16-mark structured answers with
    automatic Unit & Topic identification, page references, and bilingual support.
    """

    def _match_curriculum(self, topic: str) -> Optional[Dict[str, Any]]:
        """Finds matching curriculum topic by exact key, substring, or keyword overlap."""
        lower_topic = topic.lower().strip()
        
        # 1. Exact or substring match
        for key, entry in CURRICULUM.items():
            if key in lower_topic or lower_topic in key:
                return entry

        # 2. Token overlap after stripping query stopwords
        words = re.findall(r"[a-z0-9]+", lower_topic)
        stop_words = {
            "explain", "what", "is", "are", "the", "in", "simple", "tamil", "thanglish",
            "tell", "me", "about", "concept", "concepts", "define", "give", "notes",
            "on", "a", "an", "for", "of", "and", "please", "describe"
        }
        core_words = [w for w in words if w not in stop_words and len(w) > 1]

        for key, entry in CURRICULUM.items():
            key_clean = key.replace("/", " ")
            key_words = set(re.findall(r"[a-z0-9]+", key_clean))
            if any(cw in key_words for cw in core_words):
                return entry

        return None

    def detect_subject_and_unit(self, topic: str, subject_hint: str = "") -> Dict[str, Any]:
        """
        Analyzes a query string, matches it against known subject syllabuses
        and pinpoints the exact Unit (1-5) and official Topic.
        """
        lower_topic = topic.lower().strip()
        lower_hint = subject_hint.lower().strip() if subject_hint else ""

        # Check curriculum database first
        matched_curriculum = self._match_curriculum(topic)
        if matched_curriculum:
            return {
                "subject": matched_curriculum["subject"],
                "unit": matched_curriculum["unit"],
                "unit_title": matched_curriculum["unit_title"],
                "topic": matched_curriculum["topic"],
                "book": matched_curriculum["book"],
                "page_ref": matched_curriculum["page_ref"],
                "matched": True
            }

        # Check SUBJECT_CATALOG
        subject_key = None
        if lower_hint and lower_hint in SUBJECT_ALIASES:
            subject_key = SUBJECT_ALIASES[lower_hint]

        # Search all subject catalogs
        for s_key, s_data in SUBJECT_CATALOG.items():
            if subject_key and s_key != subject_key:
                continue
            for unit_info in s_data["units"]:
                for t in unit_info["topics"]:
                    if t in lower_topic or any(w in lower_topic for w in t.split() if len(w) > 3):
                        return {
                            "subject": s_data["name"],
                            "unit": unit_info["unit"],
                            "unit_title": unit_info["title"],
                            "topic": topic.title(),
                            "book": f"Standard Textbook for {s_data['name']}",
                            "page_ref": f"Unit {unit_info['unit']} Reference",
                            "matched": True
                        }

        # Fallback default
        sub_name = SUBJECT_CATALOG.get(subject_key, {}).get("name", subject_hint or "General Studies")
        return {
            "subject": sub_name,
            "unit": 1,
            "unit_title": "Core Foundations",
            "topic": topic.title(),
            "book": f"Prescribed Syllabus - {sub_name}",
            "page_ref": "Unit 1 - Module 1",
            "matched": False
        }

    def extract_query_intent(self, message: str, default_lang: str = "English", default_marks: int = 5):
        """Extracts desired marks and language from natural user queries."""
        lower = message.lower()
        detected_lang = default_lang
        detected_marks = default_marks

        # 1. Language detection
        if any(k in lower for k in ["in tamil", "tamil la", "tamil-la", "tamilil", "தமிழ்", "தமிழில்", "tamil"]):
            detected_lang = "Tamil"
        elif any(k in lower for k in ["in thanglish", "thanglish la", "thanglish-la", "thanglish", "tanglish", "தாங்க்லீஷ்"]):
            detected_lang = "Thanglish"
        elif any(k in lower for k in ["in english", "english la", "english"]):
            detected_lang = "English"

        # 2. Mark detection
        if re.search(r"\b1\s*(mark|marks?|மதிப்பெண்)\b", lower):
            detected_marks = 1
        elif re.search(r"\b2\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 2
        elif re.search(r"\b3\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 3
        elif re.search(r"\b5\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 5
        elif re.search(r"\b8\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 8
        elif re.search(r"\b10\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 10
        elif re.search(r"\b16\s*(marks?|mark|மதிப்பெண்)\b", lower):
            detected_marks = 16

        # Clean query to extract pure topic
        cleaned = re.sub(r"\b(explain|what is|what are|define|tell me about|notes on|give|in|simple|for|exam|university|answer|please|describe)\b", "", lower, flags=re.I)
        cleaned = re.sub(r"\b(tamil|thanglish|tanglish|english|la|sol|sollu|kudu|varanum|pannu)\b", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\b(1|2|3|5|8|10|16)\s*(marks?|mark|மதிப்பெண்)\b", "", cleaned, flags=re.I)
        cleaned = cleaned.strip()
        if not cleaned or len(cleaned) < 2:
            cleaned = message.strip()

        return cleaned, detected_marks, detected_lang

    def _normalize_lang(self, language: str) -> str:
        l = (language or "English").strip().lower()
        if "tamil" in l or "தமிழ்" in l:
            return "Tamil"
        elif "thanglish" in l or "tanglish" in l or "தாங்க்லீஷ்" in l:
            return "Thanglish"
        return "English"

    def _prepare_topic_data(self, topic: str, meta: Dict, entry: Optional[Dict]) -> Dict[str, Dict]:
        """Prepares comprehensive content in English, Tamil, and Thanglish."""
        # English
        def_en = entry.get("definition") if entry else f"{topic.title()} is a fundamental architectural concept in {meta['subject']} ({meta['unit_title']}) that standardizes functional modularity and data consistency."
        pts_en = entry.get("key_points") if entry else [
            f"Core Component 1: Primary structural block governing operational state in {meta['subject']}.",
            f"Core Component 2: Protocol standards ensuring error-free communication and data exchange.",
            f"Core Component 3: Performance optimization layer minimizing processing delay.",
            f"Core Component 4: Interfaces directly with surrounding software and hardware subsystems."
        ]
        diag = entry.get("architecture_diagram", f"[{topic.title()} Input Interface] ---> [Processing Engine] ---> [Target Output State]") if entry else f"[{topic.title()} Input Interface] ---> [Processing Engine] ---> [Target Output State]"
        adv_en = entry.get("advantages") if entry else ["High modularity and fault isolation", "Ease of debugging and system recovery", "High reliability and deterministic performance"]
        app_en = entry.get("applications", f"Standard implementation in {meta['subject']} production environments and enterprise computing.") if entry else f"Standard implementation in {meta['subject']} production environments and enterprise computing."

        # Tamil
        def_ta = entry.get("tamil_definition") if entry else f"{topic.title()} என்பது {meta['subject']} பாடத்தின் (அலகு {meta['unit']}: {meta['unit_title']}) மிக முக்கியமான அடிப்படை தொழில் நுட்ப அமைப்பாகும். இது கணினி கட்டமைப்பில் தரவு ஒருமைப்பாடு, நம்பகத்தன்மை மற்றும் சீரான செயல்பாட்டை உறுதி செய்கிறது."
        pts_ta = entry.get("tamil_points") if entry else [
            f"அடிப்படை கூறு 1: {topic.title()} கணினி அமைப்பின் மைய செயல்பாடுகளை முறைப்படுத்துகிறது.",
            f"அடிப்படை கூறு 2: தரவு பரிமாற்றத்தில் பிழைகள் ஏற்படாமல் பாதுகாக்கிறது.",
            f"அடிப்படை கூறு 3: கணினி செயலாக்க வேகத்தை அதிகரித்து தாமதத்தை (Latency) குறைக்கிறது.",
            f"அடிப்படை கூறு 4: பிற மென்பொருள் மற்றும் வன்பொருள் அடுக்குகளுடன் தடையின்றி இணைகிறது."
        ]
        adv_ta = [
            "அதிக கட்டமைப்பு நெகிழ்வுத்தன்மை மற்றும் பிழை தனிமைப்படுத்தல் (Fault Isolation)",
            "வேகமான தரவு அணுகல் மற்றும் குறைந்த கணினி வள பயன்பாடு (Resource Efficiency)",
            "பல்கலைக்கழக தேர்வு மற்றும் தொழில்முறை பயன்பாடுகளுக்கான தரநிலைகள்"
        ]
        app_ta = f"{meta['subject']} சார்ந்த தொழில்துறை மென்பொருட்கள், கிளவுட் அமைப்புகள் மற்றும் நிஜ உலக பயன்பாடுகளில் இது அடிப்படையாக உள்ளது."

        # Thanglish
        def_th = entry.get("tanglish_summary") if entry else f"{topic.title()} vandhu {meta['subject']} (Unit {meta['unit']}: {meta['unit_title']}) la oru romba mukkiyamaana core concept. Idhu system la data correct-aa process aagavum, error varaama reliable-aa run aagavum use aagudhu."
        pts_th = [
            f"Main Point 1: {topic.title()} core operations ah standardise panni system state ah manage pannum.",
            f"Main Point 2: Communication and packet transfer la errors varaama protocol check pannum.",
            f"Main Point 3: Processing delay (latency) minimize panni performance maximize pannum.",
            f"Main Point 4: Higher layers and lower hardware modules kooda smooth-aa interface aagum."
        ]
        adv_th = [
            "High modularity and easy troubleshooting (oru layer la error vandhaa easily identify pannalaam)",
            "Fast performance and optimized memory utilization",
            "Industry standard and university exams la high scoring concept"
        ]
        app_th = f"Modern cloud architecture, high-speed networks and {meta['subject']} real-world enterprise applications la widely use aagudhu."

        return {
            "en": {"def": def_en, "pts": pts_en, "diag": diag, "adv": adv_en, "app": app_en},
            "ta": {"def": def_ta, "pts": pts_ta, "diag": diag, "adv": adv_ta, "app": app_ta},
            "th": {"def": def_th, "pts": pts_th, "diag": diag, "adv": adv_th, "app": app_th}
        }

    def generate_answer(self, topic: str, marks: int, language: str = "English", subject: str = "", username: str = "Student") -> Dict[str, Any]:
        """
        Synthesizes an exam-standard answer for 1, 2, 5, 8, or 16 marks.
        Fully bilingual: When Tamil is requested, the entire answer is in Tamil.
        When Thanglish is requested, the entire answer is in Thanglish.
        """
        lang = self._normalize_lang(language)

        # Detect unit and subject metadata
        unit_meta = self.detect_subject_and_unit(topic, subject)
        curriculum_entry = self._match_curriculum(topic)

        # Check if user uploaded a book with indexed content
        doc_match = document_service.search_indexed_materials(topic, username, subject)
        if doc_match:
            unit_meta["book"] = doc_match["book"]
            unit_meta["chapter"] = doc_match.get("chapter")
            unit_meta["page_ref"] = f"Page {doc_match['page']}" if doc_match.get("page") else ""
            unit_meta["page"] = doc_match.get("page")
            unit_meta["unit"] = doc_match.get("unit", 1)

        # If OpenAI is available, generate a dynamic answer with strict language constraint
        if client:
            try:
                system_prompt = "You are ARIVORA AI, an expert academic assistant. "
                if lang == "Tamil":
                    system_prompt += "You MUST write the ENTIRE answer strictly in pure Tamil (தமிழ்) language from start to end with Tamil headings and explanations. Do not provide English sections first."
                elif lang == "Thanglish":
                    system_prompt += "You MUST write the ENTIRE answer in conversational Thanglish (Tamil written using English alphabet) from start to end with clear step-by-step headings. Do not provide English sections first."
                else:
                    system_prompt += "Provide an exam-oriented structured academic answer."

                if marks == 1:
                    system_prompt += " Provide a concise 1-mark definition and key formula."
                elif marks == 2:
                    system_prompt += " Provide a brief 2-mark definition and 2 key points."
                elif marks in [3, 4, 5]:
                    system_prompt += f" Provide a {marks}-mark explanation with definition, core working, architecture flow, advantages, and real-world example."
                elif marks in [8, 10]:
                    system_prompt += f" Provide an {marks}-mark structured answer with definition, block diagram, operational mechanism, technical specs, advantages, and exam tips."
                elif marks >= 16:
                    system_prompt += " Provide a comprehensive 16-mark university essay with 8 structured parts."

                context = ""
                if doc_match:
                    context = f"Use the following excerpt from the user's uploaded material:\n{doc_match['snippet']}\n\n"
                elif curriculum_entry:
                    context = f"Key context:\nDefinition: {curriculum_entry.get('definition', '')}\nTamil Definition: {curriculum_entry.get('tamil_definition', '')}\nKey Points: {', '.join(curriculum_entry.get('key_points', []))}\n\n"

                prompt = f"{context}Topic to explain: {topic}\nSubject context: {unit_meta['subject']}"

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1200,
                    temperature=0.6
                )
                
                generated_text = response.choices[0].message.content.strip()
                
                if lang == "Tamil":
                    header = [
                        f"📚 ARIVORA AI - {marks}-மதிப்பெண் மாதிரி விடை | தமிழ் விளக்கம்",
                        f"🎯 பாடம்: {unit_meta['subject']} | அலகு {unit_meta['unit']}: {unit_meta['unit_title']}",
                        f"📖 பாடப்புத்தகம்: {unit_meta['book']} ({unit_meta['page_ref']})",
                        "=" * 60,
                        "",
                        generated_text
                    ]
                elif lang == "Thanglish":
                    header = [
                        f"📚 ARIVORA AI - {marks}-MARK EXAM ANSWER (TANGLISH)",
                        f"🎯 Subject: {unit_meta['subject']} | Unit {unit_meta['unit']}: {unit_meta['unit_title']}",
                        f"📖 Reference: {unit_meta['book']} ({unit_meta['page_ref']})",
                        "=" * 60,
                        "",
                        generated_text
                    ]
                else:
                    header = [
                        f"📚 ARIVORA AI - {marks}-MARK EXAM-ORIENTED ANSWER",
                        f"🎯 Target Subject : {unit_meta['subject']} | Unit {unit_meta['unit']}: {unit_meta['unit_title']}",
                        f"📖 Reference      : {unit_meta['book']} ({unit_meta['page_ref']})",
                        "=" * 60,
                        "",
                        generated_text
                    ]

                return {
                    "success": True,
                    "topic": topic,
                    "marks": marks,
                    "unit": unit_meta["unit"],
                    "unit_title": unit_meta["unit_title"],
                    "subject": unit_meta["subject"],
                    "reference": f"{unit_meta['book']} | {unit_meta['page_ref']}",
                    "language": lang,
                    "answer": "\n".join(header),
                    "tamil_summary": "Generated by AI"
                }
            except Exception as e:
                print(f"OpenAI fallback notice: {e}")

        # Static deterministic generation
        data = self._prepare_topic_data(topic, unit_meta, curriculum_entry)

        if marks == 1:
            return self._build_1_mark_answer(topic, unit_meta, data, lang)
        elif marks == 2:
            return self._build_2_mark_answer(topic, unit_meta, data, lang)
        elif marks in [3, 4, 5]:
            ans = self._build_5_mark_answer(topic, unit_meta, data, lang)
            ans["marks"] = marks
            return ans
        elif marks in [8, 10]:
            ans = self._build_8_mark_answer(topic, unit_meta, data, lang)
            ans["marks"] = marks
            return ans
        elif marks >= 16:
            return self._build_16_mark_answer(topic, unit_meta, data, lang)

        return self._build_5_mark_answer(topic, unit_meta, data, lang)

    def _build_1_mark_answer(self, topic: str, meta: Dict, data: Dict, lang: str) -> Dict[str, Any]:
        """1-mark rubric: Direct definition or core formula"""
        if lang == "Tamil":
            lines = [
                f"📚 ARIVORA AI - 1-மதிப்பெண் மாதிரி விடை | தமிழ் விளக்கம்",
                f"🎯 பாடம்: {meta['subject']} | அலகு {meta['unit']}: {meta['unit_title']}",
                f"📖 பாடப்புத்தகம்: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1-மதிப்பெண் நேரடி வரையறை (Definition):",
                f"   {data['ta']['def']}",
                "",
                "முக்கிய குறிப்பு (Key Highlight):",
                f"   • {data['ta']['pts'][0]}"
            ]
        elif lang == "Thanglish":
            lines = [
                f"📚 ARIVORA AI - 1-MARK EXAM ANSWER (TANGLISH)",
                f"🎯 Subject: {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1-MARK DIRECT DEFINITION / EXPLANATION:",
                f"   {data['th']['def']}",
                "",
                "MUKKIYAMAANA POINT / FORMULA:",
                f"   • {data['th']['pts'][0]}"
            ]
        else:
            lines = [
                f"📚 ARIVORA AI - 1-MARK EXAM-ORIENTED ANSWER",
                f"🎯 Target Subject : {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference      : {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. DIRECT DEFINITION / OBJECTIVE CRITERIA:",
                f"   {data['en']['def']}",
                "",
                "2. KEY ATTRIBUTE / FORMULA:",
                f"   • {data['en']['pts'][0]}"
            ]

        return {
            "success": True,
            "topic": topic,
            "marks": 1,
            "unit": meta["unit"],
            "unit_title": meta["unit_title"],
            "subject": meta["subject"],
            "reference": f"{meta['book']} | {meta['page_ref']}",
            "language": lang,
            "answer": "\n".join(lines),
            "tamil_summary": data["ta"]["def"]
        }

    def _build_2_mark_answer(self, topic: str, meta: Dict, data: Dict, lang: str) -> Dict[str, Any]:
        """2-mark university rubric: Definition + 2 Key Points"""
        if lang == "Tamil":
            lines = [
                f"📚 ARIVORA AI - 2-மதிப்பெண் தேர்வு மாதிரி விடை | தமிழ் விளக்கம்",
                f"🎯 பாடம்: {meta['subject']} | அலகு {meta['unit']}: {meta['unit_title']}",
                f"📖 பாடப்புத்தகம்: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. வரையறை (Definition - 2 மதிப்பெண் அளவுகோல்):",
                f"   {data['ta']['def']}",
                "",
                "2. முக்கிய அம்சங்கள் (Key Points / Attributes):",
                f"   • {data['ta']['pts'][0]}",
                f"   • {data['ta']['pts'][1]}",
                "",
                "3. தேர்வு எழுதும் குறிப்பு (Exam Scoring Tip):",
                f"   பல்கலைக்கழக தேர்வில் இந்த வரையறையுடன் 2 முக்கிய குறிப்புகளையும் எழுதினால் முழு 2 மதிப்பெண்கள் பெறலாம்."
            ]
        elif lang == "Thanglish":
            lines = [
                f"📚 ARIVORA AI - 2-MARK EXAM ANSWER (TANGLISH)",
                f"🎯 Subject: {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. DEFINITION (2 Marks Criteria):",
                f"   {data['th']['def']}",
                "",
                "2. MUKKIYAMAANA 2 POINTS (Key Attributes):",
                f"   • {data['th']['pts'][0]}",
                f"   • {data['th']['pts'][1]}",
                "",
                "3. EXAM SCORING TIP:",
                f"   University exam answer sheet la indha definition kooda serthu indha 2 points ezhudhinaa full 2 marks easy-aa score pannalaam."
            ]
        else:
            lines = [
                f"📚 ARIVORA AI - 2-MARK EXAM-ORIENTED ANSWER",
                f"🎯 Target Subject : {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference      : {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. DEFINITION (2 Marks Criteria):",
                f"   {data['en']['def']}",
                "",
                "2. KEY POINTS / ATTRIBUTES:",
                f"   • {data['en']['pts'][0]}",
                f"   • {data['en']['pts'][1]}",
                "",
                "3. EXAM SCORING TIP:",
                f"   State the formal definition along with these two bullet points for full university marks."
            ]

        return {
            "success": True,
            "topic": topic,
            "marks": 2,
            "unit": meta["unit"],
            "unit_title": meta["unit_title"],
            "subject": meta["subject"],
            "reference": f"{meta['book']} | {meta['page_ref']}",
            "language": lang,
            "answer": "\n".join(lines),
            "tamil_summary": data["ta"]["def"]
        }

    def _build_5_mark_answer(self, topic: str, meta: Dict, data: Dict, lang: str) -> Dict[str, Any]:
        """5-mark rubric: Definition, Core working, Diagram, Advantages, Real-world example"""
        if lang == "Tamil":
            lines = [
                f"📚 ARIVORA AI - 5-மதிப்பெண் மாதிரி விடை | தமிழ் விளக்கம்",
                f"🎯 பாடம்: {meta['subject']} | அலகு {meta['unit']}: {meta['unit_title']}",
                f"📖 பாடப்புத்தகம்: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. முழுமையான வரையறை (Formal Definition):",
                f"   {data['ta']['def']}",
                "",
                "2. செயல்பாட்டுக் கொள்கை மற்றும் முக்கிய கூறுகள் (Core Principles & Working):",
            ]
            for p in data['ta']['pts'][:4]:
                lines.append(f"   • {p}")
            lines.extend([
                "",
                "3. கட்டமைப்பு வரைபடம் / மாதிரி (Architecture Diagram / Flow):",
                data['ta']['diag'],
                "",
                "4. முக்கிய நன்மைகள் (Key Advantages):",
                f"   1. {data['ta']['adv'][0]}",
                f"   2. {data['ta']['adv'][1]}",
                "",
                "5. நிஜ உலக பயன்பாடு / உதாரணம் (Real-World Example):",
                f"   {data['ta']['app']}"
            ])
        elif lang == "Thanglish":
            lines = [
                f"📚 ARIVORA AI - 5-MARK EXAM ANSWER (TANGLISH)",
                f"🎯 Subject: {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. FORMAL DEFINITION & OVERVIEW:",
                f"   {data['th']['def']}",
                "",
                "2. STEP-BY-STEP WORKING & CORE POINTS:",
            ]
            for p in data['th']['pts'][:4]:
                lines.append(f"   • {p}")
            lines.extend([
                "",
                "3. ARCHITECTURE DIAGRAM / FLOW:",
                data['th']['diag'],
                "",
                "4. MUKKIYAMAANA NALMAIGAL (KEY ADVANTAGES):",
                f"   1. {data['th']['adv'][0]}",
                f"   2. {data['th']['adv'][1]}",
                "",
                "5. REAL-WORLD USAGE / EXAMPLE:",
                f"   {data['th']['app']}"
            ])
        else:
            lines = [
                f"📚 ARIVORA AI - 5-MARK EXAM-ORIENTED ANSWER",
                f"🎯 Target Subject : {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference      : {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. FORMAL DEFINITION:",
                f"   {data['en']['def']}",
                "",
                "2. CORE PRINCIPLES & WORKING:",
            ]
            for p in data['en']['pts'][:4]:
                lines.append(f"   • {p}")
            lines.extend([
                "",
                "3. STRUCTURAL ARCHITECTURE / FLOW:",
                data['en']['diag'],
                "",
                "4. KEY ADVANTAGES & SIGNIFICANCE:",
                f"   1. {data['en']['adv'][0]}",
                f"   2. {data['en']['adv'][1]}",
                "",
                "5. REAL-WORLD EXAMPLE / CASE STUDY:",
                f"   {data['en']['app']}"
            ])

        return {
            "success": True,
            "topic": topic,
            "marks": 5,
            "unit": meta["unit"],
            "unit_title": meta["unit_title"],
            "subject": meta["subject"],
            "reference": f"{meta['book']} | {meta['page_ref']}",
            "language": lang,
            "answer": "\n".join(lines),
            "tamil_summary": data["ta"]["def"]
        }

    def _build_8_mark_answer(self, topic: str, meta: Dict, data: Dict, lang: str) -> Dict[str, Any]:
        """8-mark university rubric: Deep breakdown, Diagram, Steps, Protocols, Advantages, Exam Tips"""
        if lang == "Tamil":
            lines = [
                f"📚 ARIVORA AI - 8-மதிப்பெண் விரிவான தேர்வு மாதிரி விடை | தமிழ் விளக்கம்",
                f"🎯 பாடம்: {meta['subject']} | அலகு {meta['unit']}: {meta['unit_title']}",
                f"📖 பாடப்புத்தகம்: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. விரிவான அறிமுகம் மற்றும் கோட்பாட்டு விளக்கம் (Introduction & Concept):",
                f"   {data['ta']['def']}",
                f"   {meta['subject']} பாடத்திட்டத்தின் அலகு {meta['unit']}-ல் {topic.title()} ஒரு முக்கிய தொழில்நுட்ப அமைப்பாகும்.",
                "",
                "2. கட்டமைப்பு மாதிரி வரைபடம் (Architectural Block Diagram):",
                data['ta']['diag'],
                "",
                "3. படிப்படியான செயல்பாட்டு நிலைகள் (Step-by-Step Working Mechanism):",
            ]
            for idx, p in enumerate(data['ta']['pts'], 1):
                lines.append(f"   நிலை {idx}: {p}")
            lines.extend([
                "",
                "4. தொழில்நுட்ப நெறிமுறைகள் மற்றும் பண்புகள் (Technical Specifications):",
                "   • நேரம் மற்றும் செயலாக்க வேகம் (Latency & Throughput): மிகக் குறைந்த தாமதத்துடன் அதிக செயல்திறன்.",
                "   • நம்பகத்தன்மை (Reliability & Fault Tolerance): பிழைகளை கண்டறிந்து தானாக மீட்டெடுக்கும் முறை.",
                "",
                "5. முக்கிய நன்மைகள் மற்றும் சவால்கள் (Advantages & Limitations):",
                f"   [+] நன்மைகள்: {data['ta']['adv'][0]}, {data['ta']['adv'][1]}.",
                "   [-] சவால்கள்: குறைந்த அலைவரிசை சூழல்களில் கூடுதல் தலைப்பு மேல்நிலை (Header Overhead).",
                "",
                "6. நிஜ உலக பயன்பாடு மற்றும் தேர்வு உத்திகள் (Real-World Use & Exam Scoring):",
                f"   • பயன்பாடு: {data['ta']['app']}",
                "   • தேர்வு உத்தி: பரீட்சையில் தலைப்புகளை அடிக்கோடிட்டு காட்டி, வரைபடத்தை தெளிவாக வரைவது அதிக மதிப்பெண் பெற்றுத்தரும்."
            ])
        elif lang == "Thanglish":
            lines = [
                f"📚 ARIVORA AI - 8-MARK EXAM ANSWER (TANGLISH)",
                f"🎯 Subject: {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference: {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. INTRODUCTION & COMPLETE DEFINITION:",
                f"   {data['th']['def']}",
                f"   Idhu {meta['subject']} syllabus Unit {meta['unit']} ({meta['unit_title']}) la varra high-priority exam question.",
                "",
                "2. ARCHITECTURAL BLOCK DIAGRAM:",
                data['th']['diag'],
                "",
                "3. STEP-BY-STEP WORKING FLOW:",
            ]
            for idx, p in enumerate(data['th']['pts'], 1):
                lines.append(f"   Step {idx}: {p}")
            lines.extend([
                "",
                "4. TECHNICAL PROTOCOL & SYSTEM ATTRIBUTES:",
                "   • Speed & Latency: Fast execution and optimized memory usage ensure pannum.",
                "   • Error Handling: Data flow la error varaama automated check and recovery pannum.",
                "",
                "5. ADVANTAGES & LIMITATIONS (Nalmaigal & Sawaalgal):",
                f"   [+] Advantages: {data['th']['adv'][0]}, {data['th']['adv'][1]}.",
                "   [-] Limitations: High-volume network la header overhead or configuration complexity irukkalaam.",
                "",
                "6. REAL-WORLD EXAMPLE & EXAM TIPS:",
                f"   • Application: {data['th']['app']}",
                "   • Exam Scoring Tip: Exam sheet la diagram neat-aa pencil la potte parts label panninaa high marks score pannalaam."
            ])
        else:
            lines = [
                f"📚 ARIVORA AI - 8-MARK DETAILED EXAM ANSWER",
                f"🎯 Target Subject : {meta['subject']} | Unit {meta['unit']}: {meta['unit_title']}",
                f"📖 Reference      : {meta['book']} ({meta['page_ref']})",
                "=" * 60,
                "",
                "1. FORMAL INTRODUCTION & THEORETICAL OVERVIEW:",
                f"   {data['en']['def']}",
                f"   Within {meta['subject']} ({meta['unit_title']}), {topic.title()} is a central concept for state management and protocol architecture.",
                "",
                "2. ARCHITECTURAL BLOCK DIAGRAM:",
                data['en']['diag'],
                "",
                "3. STEP-BY-STEP OPERATIONAL MECHANISM:",
            ]
            for idx, p in enumerate(data['en']['pts'], 1):
                lines.append(f"   Stage {idx}: {p}")
            lines.extend([
                "",
                "4. TECHNICAL PROTOCOLS & SPECIFICATIONS:",
                "   • Throughput & Latency: Pipelined execution minimizing transport delay.",
                "   • Fault Tolerance: Deterministic checksums and error recovery mechanisms.",
                "",
                "5. COMPARATIVE ADVANTAGES & LIMITATIONS:",
                f"   [+] Advantages: {data['en']['adv'][0]}, {data['en']['adv'][1]}.",
                "   [-] Limitations: Minor header encapsulation overhead in bandwidth-constrained networks.",
                "",
                "6. REAL-WORLD INDUSTRIAL APPLICATION & EXAM STRATEGY:",
                f"   • Application: {data['en']['app']}",
                "   • Exam Strategy: Draw the block diagram neatly and highlight all core stages to secure full marks."
            ])

        return {
            "success": True,
            "topic": topic,
            "marks": 8,
            "unit": meta["unit"],
            "unit_title": meta["unit_title"],
            "subject": meta["subject"],
            "reference": f"{meta['book']} | {meta['page_ref']}",
            "language": lang,
            "answer": "\n".join(lines),
            "tamil_summary": data["ta"]["def"]
        }

    def _build_16_mark_answer(self, topic: str, meta: Dict, data: Dict, lang: str) -> Dict[str, Any]:
        """16-mark university rubric: Full 8-part comprehensive academic dissertation answer"""
        if lang == "Tamil":
            lines = [
                "╔" + "═" * 68 + "╗",
                f"║  ARIVORA AI - 16-மதிப்பெண் விரிவான பல்கலைக்கழக கட்டுரை விடை | தமிழ் விளக்கம்  ║",
                f"║  பாடம்  : {meta['subject']:<20} அலகு {meta['unit']}: {meta['unit_title'][:25]:<25} ║",
                f"║  புத்தகம்: {meta['book'][:30]:<30} {meta['page_ref']:<22} ║",
                "╚" + "═" * 68 + "╝",
                "",
                "பகுதி 1: அறிமுகம் மற்றும் கோட்பாட்டு வரையறை (PART 1: INTRODUCTION)",
                "----------------------------------------------------------------------",
                f"{data['ta']['def']}",
                f"{meta['subject']} பாடத்திட்டத்தின் அலகு {meta['unit']} ({meta['unit_title']}) பிரிவில், {topic.title()} என்பது பல்கலைக்கழக தேர்வுகளில் கேட்கப்படும் முதன்மையான 16-மதிப்பெண் வினாவாகும்.",
                "",
                "பகுதி 2: விரிவான கட்டமைப்பு வரைபடம் (PART 2: DETAILED ARCHITECTURAL BLOCK DIAGRAM)",
                "----------------------------------------------------------------------",
                data['ta']['diag'],
                "",
                "பகுதி 3: படிப்படியான செயல்பாட்டுக் கொள்கை மற்றும் நிலைகள் (PART 3: WORKING PRINCIPLES)",
                "----------------------------------------------------------------------",
            ]
            for idx, pt in enumerate(data['ta']['pts'], 1):
                lines.append(f"  படி {idx}. {pt}")
            lines.extend([
                "",
                "பகுதி 4: கணித மாதிரி மற்றும் நெறிமுறை அமைப்பு (PART 4: FORMULATION & PROTOCOLS)",
                "----------------------------------------------------------------------",
                "  • கணித மாதிரி சமன்பாடு (Mathematical Invariant):",
                f"    எந்தவொரு உள்ளீட்டு பரிவர்த்தனை X மற்றும் கணினி நிலை S-க்கும்: S' = f(S, X).",
                "  • நேர சிக்கல்தன்மை (Time Complexity): O(log N) முதல் O(N) வரை உகந்த செயலாக்க நிலை.",
                "  • நினைவக பயன்பாடு (Space Complexity): O(1) கூடுதல் நினைவகம் மட்டுமே தேவைப்படுகிறது.",
                "",
                "பகுதி 5: ஒப்பீட்டு பண்புகள் அட்டவணை (PART 5: COMPARATIVE ANALYSIS TABLE)",
                "----------------------------------------------------------------------",
                "| அளவுரு (Parameter)       | பாரம்பரிய முறை (Traditional) | நவீன கட்டமைப்பு (Modern Architecture) |",
                "|-------------------------|--------------------------|-------------------------------------|",
                "| பிழை தடுக்கும் திறன்     | குறைவு (Manual Retry)    | அதிகம் (Automated Checksum / ACK)   |",
                "| செயலாக்க வேகம் / தாமதம்  | அதிக தாமதம் (High Delay) | மில்லி விநாடிக்குள் விரைவானது        |",
                "| வள பயன்பாடு             | ஒற்றை கட்டமைப்பு         | விநியோகிக்கப்பட்ட கட்டமைப்பு         |",
                "",
                "பகுதி 6: தொழில்முறை பயன்பாடுகள் (PART 6: REAL-WORLD APPLICATIONS & CASE STUDIES)",
                "----------------------------------------------------------------------",
                f"  1. நவீன மென்பொருள் பொறியியல்: கிளவுட் தளங்கள் மற்றும் அதிவேக தரவுத்தளங்களில் பயன்படுத்தப்படுகிறது.",
                f"  2. தொலைத்தொடர்பு மற்றும் நெட்வொர்க் கட்டமைப்பு: IEEE மற்றும் ISO தரநிலைகளுக்கு உட்பட்டது.",
                f"  3. நிறுவன அமைப்புகள்: தரவு இழப்பு இல்லாத பாதுகாப்பான பரிவர்த்தனையை உறுதி செய்கிறது.",
                "",
                "பகுதி 7: நன்மைகள் மற்றும் குறைபாடுகள் (PART 7: ADVANTAGES AND LIMITATIONS)",
                "----------------------------------------------------------------------",
                "  [+] நன்மைகள்:",
                f"      • {data['ta']['adv'][0]}.",
                f"      • {data['ta']['adv'][1]}.",
                "      • பிழைகளை எளிதில் கண்டறிந்து தனிமைப்படுத்தலாம்.",
                "  [-] சவால்கள் / குறைபாடுகள்:",
                "      • நெறிமுறை தலைப்பு மேல்நிலை (Header encapsulation overhead).",
                "      • துல்லியமான கட்டமைப்பு விதிமுறைகளை பின்பற்ற வேண்டும்.",
                "",
                "பகுதி 8: தேர்வு முடிவுரை மற்றும் உத்திகள் (PART 8: EXAM CONCLUSION & TOP SCORING HIGHLIGHTS)",
                "----------------------------------------------------------------------",
                "  • விடைத்தாளில் முழு மதிப்பெண் பெற கவனிக்க வேண்டியவை:",
                f"    1. {topic.title()} குறித்த தரநிலைகளை தெளிவாக குறிப்பிடவும்.",
                "    2. பகுதி 2-ல் உள்ள கட்டமைப்பு வரைபடத்தை பென்சிலால் பாகங்களுடன் வரையவும்.",
                "    3. அனைத்து 8 தலைப்புகளையும் வரிசைப்படி எழுதி விடையை நிறைவு செய்யவும்.",
                ""
            ])
        elif lang == "Thanglish":
            lines = [
                "╔" + "═" * 68 + "╗",
                f"║  ARIVORA AI - 16-MARK COMPREHENSIVE UNIVERSITY ESSAY (TANGLISH)     ║",
                f"║  Subject : {meta['subject']:<20} Unit {meta['unit']}: {meta['unit_title'][:25]:<25} ║",
                f"║  Reference: {meta['book'][:30]:<30} {meta['page_ref']:<22} ║",
                "╚" + "═" * 68 + "╝",
                "",
                "PART 1: INTRODUCTION & THEORY DEFINITION",
                "----------------------------------------------------------------------",
                f"{data['th']['def']}",
                f"{meta['subject']} syllabus ({meta['unit_title']}) la {topic.title()} vandhu Anna University & Board exams la frequent-aa kekkura high-scoring 16-mark big question.",
                "",
                "PART 2: DETAILED ARCHITECTURAL BLOCK DIAGRAM",
                "----------------------------------------------------------------------",
                data['th']['diag'],
                "",
                "PART 3: STEP-BY-STEP WORKING PRINCIPLES",
                "----------------------------------------------------------------------",
            ]
            for idx, pt in enumerate(data['th']['pts'], 1):
                lines.append(f"  Step {idx}. {pt}")
            lines.extend([
                "",
                "PART 4: MATHEMATICAL MODEL & PROTOCOL LOGIC",
                "----------------------------------------------------------------------",
                "  • Mathematical Invariant Equation:",
                f"    Given state S and input vector X: S' = f(S, X).",
                "  • Execution Complexity: O(log N) to O(N) optimized pipeline.",
                "  • Buffer & Memory Footprint: O(1) auxiliary space beyond communication frame.",
                "",
                "PART 5: COMPARATIVE ANALYSIS TABLE",
                "----------------------------------------------------------------------",
                "| Parameter               | Traditional Approach     | Modern Architectural Implementation |",
                "|-------------------------|--------------------------|-------------------------------------|",
                "| Error Resilience        | Low (Manual Retry)       | High (Automated Checksum / ACK)     |",
                "| Throughput Latency      | High Processing Delay    | Sub-millisecond Pipeline            |",
                "| Resource Consumption    | Monolithic Heavyweight   | Distributed & Modular               |",
                "",
                "PART 6: REAL-WORLD APPLICATIONS & CASE STUDIES",
                "----------------------------------------------------------------------",
                f"  1. Industrial Engineering: Applied across modern cloud platforms and high-availability systems.",
                f"  2. Telecom & Data Infrastructure: Standardized by IEEE, ISO, and IETF governing bodies.",
                f"  3. Enterprise Data Pipelines: Zero data loss and high consistency guarantee pannum.",
                "",
                "PART 7: ADVANTAGES AND LIMITATIONS (PROS & CONS)",
                "----------------------------------------------------------------------",
                "  [+] ADVANTAGES:",
                f"      • {data['th']['adv'][0]}.",
                f"      • {data['th']['adv'][1]}.",
                "      • Comprehensive telemetry and diagnostics.",
                "  [-] LIMITATIONS:",
                "      • Header encapsulation overhead in low-bandwidth networks.",
                "      • Strict protocol adherence required.",
                "",
                "PART 8: EXAM CONCLUSION & TOP SCORING HIGHLIGHTS",
                "----------------------------------------------------------------------",
                "  • Key takeaways to score full 16 marks in answer sheet:",
                f"    1. Mention the standard definition of {topic.title()}.",
                "    2. Draw the neat labelled block diagram shown in Part 2.",
                "    3. Enumerate all 8 parts with clear subheadings in your booklet.",
                ""
            ])
        else:
            lines = [
                "╔" + "═" * 68 + "╗",
                f"║  ARIVORA AI - 16-MARK COMPREHENSIVE UNIVERSITY ESSAY ANSWER         ║",
                f"║  Subject : {meta['subject']:<20} Unit {meta['unit']}: {meta['unit_title'][:25]:<25} ║",
                f"║  Reference: {meta['book'][:30]:<30} {meta['page_ref']:<22} ║",
                "╚" + "═" * 68 + "╝",
                "",
                "PART 1: INTRODUCTION & FORMAL DEFINITION",
                "----------------------------------------------------------------------",
                f"{data['en']['def']}",
                f"In the context of the {meta['subject']} syllabus ({meta['unit_title']}), {topic.title()} forms the bedrock for analyzing design trade-offs, theoretical paradigms, and enterprise engineering applications.",
                "",
                "PART 2: DETAILED ARCHITECTURAL BLOCK DIAGRAM",
                "----------------------------------------------------------------------",
                data['en']['diag'],
                "",
                "PART 3: STEP-BY-STEP WORKING PRINCIPLES",
                "----------------------------------------------------------------------",
            ]
            for idx, pt in enumerate(data['en']['pts'], 1):
                lines.append(f"  Step {idx}. {pt}")
            lines.extend([
                "",
                "PART 4: MATHEMATICAL / PROTOCOL FORMULATION & CODE LOGIC",
                "----------------------------------------------------------------------",
                "  • Mathematical Model / Invariant:",
                f"    For any given transaction state S and input vector X: S' = f(S, X).",
                "  • Standard Time Complexity: O(log N) to O(N) depending on balancing conditions.",
                "  • Space Complexity: O(1) auxiliary space beyond protocol buffer allocation.",
                "",
                "PART 5: COMPARATIVE ANALYSIS & FEATURES TABLE",
                "----------------------------------------------------------------------",
                "| Parameter               | Traditional Approach     | Modern Architectural Implementation |",
                "|-------------------------|--------------------------|-------------------------------------|",
                "| Error Resilience        | Low (Manual Retry)       | High (Automated Checksum / ACK)     |",
                "| Throughput Latency      | High Processing Delay    | Sub-millisecond Pipeline            |",
                "| Resource Consumption    | Monolithic Heavyweight   | Distributed & Modular               |",
                "",
                "PART 6: REAL-WORLD APPLICATIONS & CASE STUDIES",
                "----------------------------------------------------------------------",
                f"  1. Industrial Engineering: Applied across modern cloud platforms and high-availability systems.",
                f"  2. Telecom & Data Infrastructure: Standardized by IEEE, ISO, and IETF governing bodies.",
                f"  3. Enterprise Data Pipelines: Ensures zero data loss and compliance with academic benchmark standards.",
                "",
                "PART 7: ADVANTAGES AND LIMITATIONS",
                "----------------------------------------------------------------------",
                "  [+] ADVANTAGES:",
                f"      • {data['en']['adv'][0]}.",
                f"      • {data['en']['adv'][1]}.",
                "      • Comprehensive telemetry and diagnostics.",
                "  [-] LIMITATIONS:",
                "      • Header encapsulation overhead in minimal bandwidth environments.",
                "      • Implementation complexity requires strict protocol adherence.",
                "",
                "PART 8: EXAM CONCLUSION & TOP SCORING HIGHLIGHTS",
                "----------------------------------------------------------------------",
                "  • Key takeaways to highlight in answer booklet:",
                f"    1. Mention the ISO / IEEE standard governing {topic.title()}.",
                "    2. Draw the neat labelled block diagram shown in Part 2.",
                "    3. Enumerate all layers / steps clearly with appropriate subheadings.",
                ""
            ])

        return {
            "success": True,
            "topic": topic,
            "marks": 16,
            "unit": meta["unit"],
            "unit_title": meta["unit_title"],
            "subject": meta["subject"],
            "reference": f"{meta['book']} | {meta['page_ref']}",
            "language": lang,
            "answer": "\n".join(lines),
            "tamil_summary": data["ta"]["def"]
        }


    def generate_general_ai_answer(self, topic: str, language: str = "English") -> str:
        """
        Universal General AI Response generator for topics outside the official syllabus.
        Provides comprehensive real-world conceptual knowledge.
        """
        lang = self._normalize_lang(language)
        title = topic.strip().title()

        if client:
            try:
                system_prompt = (
                    "You are a Universal General AI Educational Mentor. "
                    "The student is asking about a topic outside their college syllabus. "
                    "Explain this topic clearly, accurately, with real-world industry examples, practical significance, and simple analogies."
                )
                if lang == "Tamil":
                    system_prompt += " Write the response strictly in clear, academic Tamil (தமிழ்)."
                elif lang == "Thanglish":
                    system_prompt += " Write the response strictly in friendly conversational Thanglish (Tamil in English alphabet)."

                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Explain the concept of: '{topic}'"}
                    ],
                    max_tokens=600,
                    temperature=0.7
                )
                return resp.choices[0].message.content
            except Exception as e:
                print(f"OpenAI General AI fallback: {e}")

        # Deterministic rich General AI answer
        if lang == "Tamil":
            return (
                f"🤖 பொதுவான AI விளக்கம் (General AI Mentor):\n"
                f"📌 தலைப்பு: {title}\n"
                f"──────────────────────────────────────────────────\n"
                f"1. பொது அறிமுகம் (Overview):\n"
                f"   '{title}' என்பது உங்கள் செமஸ்டர் பாடத்திட்டத்தில் இல்லாத ஒரு பொதுவான தொழில்நுட்பக் கருத்து. "
                f"இது உலகளாவிய கணினி அறிவியல் மற்றும் தொழில்முறை மென்பொருள் துறையில் பரவலாகப் பயன்படுகிறது.\n\n"
                f"2. முக்கிய அம்சங்கள் (Key Highlights):\n"
                f"   • அடிப்படை செயல்பாடு: தரவு மேலாண்மை மற்றும் கணினி அமைப்புகளின் செயல்திறனை முறைப்படுத்துகிறது.\n"
                f"   • தொழில்முறை முக்கியத்துவம்: நவீன கிளவுட் மற்றும் மென்பொருள் நிறுவனங்கள் இந்த தொழில்நுட்பத்தை நம்பியுள்ளன.\n\n"
                f"3. நிஜ உலக பயன்பாடு (Real-world Application):\n"
                f"   உயர் செயல்திறன் கொண்ட உற்பத்தி தளங்களில் (Enterprise Production Systems) சிக்கலான பணிகளை எளிமையாக்க {title} உதவுகிறது.\n\n"
                f"💡 குறிப்பு: இது உங்கள் கல்லூரிப் பாடத்திட்டத்திற்கு அப்பாற்பட்ட பொது அறிவுத் தகவலாகும்."
            )
        elif lang == "Thanglish":
            return (
                f"🤖 General AI Explanation (Mentor Mode):\n"
                f"📌 Topic: {title}\n"
                f"──────────────────────────────────────────────────\n"
                f"1. General Concept Overview:\n"
                f"   '{title}' vandhu unga semester syllabus la illaatha general industry topic. "
                f"Aana tech world and software development la idhu romba widely used concept!\n\n"
                f"2. Core Working & Benefits:\n"
                f"   • Basic Function: System efficiency optimize panni data workflow smooth-aa manage pannum.\n"
                f"   • Industry Importance: Modern software products and high-scale systems la idhu core building block.\n\n"
                f"3. Real-world Usage:\n"
                f"   Cloud engineering and developer tools la {title} widely implement aagudhu.\n\n"
                f"💡 Note: Idhu unga official syllabus la illaatha topic, General AI knowledge base vazhiyaaga clarify pannappattadhu."
            )
        else:
            return (
                f"🤖 Universal General AI Explanation:\n"
                f"📌 Topic: {title}\n"
                f"──────────────────────────────────────────────────\n"
                f"1. Conceptual Overview:\n"
                f"   '{title}' is an industry-standard technical concept that is not covered in your prescribed university syllabus. "
                f"However, it is extensively used in modern software engineering and enterprise technology.\n\n"
                f"2. Key Working Principles:\n"
                f"   • Architectural Role: Manages system execution states, structural modularity, and operational workflows.\n"
                f"   • Reliability & Scaling: Enables distributed nodes to synchronize efficiently without bottlenecking.\n\n"
                f"3. Industry Applications:\n"
                f"   Widely deployed across modern cloud architectures, scalable backends, and cutting-edge software solutions.\n\n"
                f"💡 Note: This explanation was answered by General AI since this topic is outside your semester syllabus."
            )

ai_engine = AIEngine()
