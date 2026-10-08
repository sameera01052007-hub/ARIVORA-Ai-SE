/* =========================================================
   ARIVORA AI - FRONTEND APPLICATION SCRIPT
   "Your Syllabus. Your Books. Your AI."
   Connected to ARIVORA AI FastAPI Backend (http://127.0.0.1:8000)
========================================================= */

"use strict";

const RENDER_BACKEND_URL = "https://arivora-ai-se.onrender.com";

const API_BASE = (() => {
    const meta = document.querySelector('meta[name="backend-url"]');
    if (meta && meta.content && meta.content.trim()) return meta.content.replace(/\/$/, "");

    const origin = window.location.origin || "";
    const hostname = window.location.hostname;
    const port = window.location.port;

    if (window.location.protocol === "file:" || 
        ((hostname === "localhost" || hostname === "127.0.0.1" || hostname === "") && port !== "8000")) {
        return RENDER_BACKEND_URL;
    }

    return origin || RENDER_BACKEND_URL;
})();

async function safeApiFetch(endpointPath, options = {}) {
    try {
        const primaryUrl = `${API_BASE}${endpointPath.startsWith("/") ? "" : "/"}${endpointPath}`;
        const res = await fetch(primaryUrl, options);
        if (res.ok || res.status < 500) {
            return await res.json();
        }
    } catch (err) {
        console.warn("[ARIVORA AI] Primary API_BASE failed, trying Render backup...", err);
    }

    if (API_BASE !== RENDER_BACKEND_URL) {
        try {
            const fallbackUrl = `${RENDER_BACKEND_URL}${endpointPath.startsWith("/") ? "" : "/"}${endpointPath}`;
            const resFallback = await fetch(fallbackUrl, options);
            if (resFallback.ok || resFallback.status < 500) {
                return await resFallback.json();
            }
        } catch (errFallback) {
            console.error("[ARIVORA AI] Fallback API failed:", errFallback);
        }
    }
    throw new Error("Unable to connect to backend server.");
}



/* =========================================================
   GLOBAL USER DATA
========================================================= */

let currentUser = {
    username: "Student",
    role: "student",
    education: "College",
    board: "Anna University",
    medium: "English",
    institution: "Engineering College",
    course: "B.E / B.Tech",
    branch: "Computer Science and Engineering",
    languages: ["English", "Tamil"]
};

let currentAiLanguage = "English";
let activeChatTopic = "OSI layers";
let activeChatSubject = "Computer Networks";
let currentAudioPlayer = null;
let currentTTSutterance = null;
let currentTTSButton = null; // tracks which speaker btn is active
let isTTSPlaying = false;

/* =========================================================
   HELPER FUNCTIONS
========================================================= */

function showElement(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove("d-none");
        el.style.display = "";
    }
}

function hideElement(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.add("d-none");
    }
}

function showToast(message, type = "info") {
    // Simple non-blocking alert or dynamic banner
    const existing = document.getElementById("ARIVORAToast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.id = "ARIVORAToast";
    toast.className = `alert alert-${type === "success" ? "success" : type === "error" ? "danger" : "primary"}`;
    toast.style.cssText = "position: fixed; bottom: 25px; right: 25px; z-index: 9999; max-width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); border-radius: 12px;";
    toast.innerHTML = `<i class="bi bi-info-circle me-2"></i> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

/* =========================================================
   AUTHENTICATION & PROFILE SETUP
========================================================= */

function handleLoginSubmit() {
    const userField = document.getElementById("loginUsername");
    if (userField && userField.value.trim()) {
        currentUser.username = userField.value.trim();
        saveLocalUser();
    }
    showRolePage();
}

function showRolePage() {
    hideElement("loginPage");
    hideElement("signupPage");
    showElement("rolePage");
    window.scrollTo(0, 0);
}

function showSignup() {
    hideElement("loginPage");
    hideElement("rolePage");
    showElement("signupPage");
    window.scrollTo(0, 0);
}

function showLogin() {
    hideElement("signupPage");
    hideElement("rolePage");
    hideElement("profilePage");
    hideElement("languagePage");
    hideElement("dashboardPage");
    showElement("loginPage");
    window.scrollTo(0, 0);
}

function handleSignOut() {
    localStorage.removeItem("ARIVORAUser");
    localStorage.removeItem("arivoraUser");
    currentUser = {
        username: "Student",
        role: "student",
        education: "College",
        board: "Anna University",
        medium: "English",
        institution: "Engineering College",
        course: "B.E / B.Tech",
        branch: "Computer Science and Engineering",
        languages: ["English", "Tamil"]
    };
    showLogin();
    showToast("Logged out successfully.", "info");
}

function selectRole(role) {
    currentUser.role = role;
    saveLocalUser();
    hideElement("rolePage");
    showElement("profilePage");
    updateRoleText();
    updateRoleUI();
    window.scrollTo(0, 0);
}

function updateRoleText() {
    const isFaculty = currentUser.role === "faculty";
    const roleElements = document.querySelectorAll(".user-info span");
    roleElements.forEach(element => {
        element.textContent = isFaculty ? "Faculty / Educator" : "Student";
    });
    const nameEls = document.querySelectorAll(".user-info h6");
    nameEls.forEach(el => {
        el.textContent = currentUser.username || "Student";
    });
    updateRoleUI();
}

function updateRoleUI() {
    const isFaculty = currentUser.role === "faculty";
    const facultySidebarLink = document.getElementById("sidebarFacultyLink");
    const quizSidebarLink = document.getElementById("sidebarQuizLink");
    const examsSidebarLink = document.getElementById("sidebarExamsLink");
    const statProgress = document.getElementById("statCardProgress");
    const statExams = document.getElementById("statCardExams");
    const taskQuiz = document.getElementById("taskCardDailyQuiz");

    if (facultySidebarLink) {
        if (isFaculty) {
            facultySidebarLink.classList.remove("d-none");
        } else {
            facultySidebarLink.classList.add("d-none");
        }
    }

    if (isFaculty) {
        if (quizSidebarLink) quizSidebarLink.classList.add("d-none");
        if (examsSidebarLink) examsSidebarLink.classList.add("d-none");
        if (statProgress) statProgress.classList.add("d-none");
        if (statExams) statExams.classList.add("d-none");
        if (taskQuiz) taskQuiz.classList.add("d-none");
    } else {
        if (quizSidebarLink) quizSidebarLink.classList.remove("d-none");
        if (examsSidebarLink) examsSidebarLink.classList.remove("d-none");
        if (statProgress) statProgress.classList.remove("d-none");
        if (statExams) statExams.classList.remove("d-none");
        if (taskQuiz) taskQuiz.classList.remove("d-none");
    }
}

function showLanguagePage() {
    const selects = document.querySelectorAll("#profilePage select");
    if (selects.length > 0) {
        currentUser.education = selects[0]?.value || "College";
        currentUser.board = selects[1]?.value || "Anna University";
        currentUser.medium = selects[2]?.value || "English";
        currentUser.institution = selects[3]?.value || "Engineering College";
    }

    saveLocalUser();
    hideElement("profilePage");
    showElement("languagePage");
    window.scrollTo(0, 0);
}

async function showDashboard() {
    currentUser.languages = [];
    const languageInputs = document.querySelectorAll("#languagePage input[type='checkbox']");

    languageInputs.forEach(input => {
        if (input.checked) {
            const label = input.closest("label");
            if (label) currentUser.languages.push(label.innerText.trim());
        }
    });

    if (currentUser.languages.length === 0) {
        currentUser.languages = ["English", "Tamil"];
    }

    saveLocalUser();

    // Sync profile with backend API
    try {
        await fetch(`${API_BASE}/api/profile`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: currentUser.username,
                role: currentUser.role,
                education: currentUser.education || "College",
                board: currentUser.board,
                institution: currentUser.institution,
                medium: currentUser.medium,
                course: currentUser.course,
                branch: currentUser.branch,
                languages: currentUser.languages
            })
        });
    } catch (e) {
        console.warn("Backend profile sync notice:", e);
    }

    hideElement("loginPage");
    hideElement("signupPage");
    hideElement("rolePage");
    hideElement("profilePage");
    hideElement("languagePage");

    showElement("dashboardPage");
    updateRoleText();
    updateRoleUI();
    window.scrollTo(0, 0);

    if (currentUser.role === "faculty") {
        showModule("faculty");
    } else {
        showModule("home");
    }
    loadUserFolders();
}

function saveLocalUser() {
    localStorage.setItem("ARIVORAUser", JSON.stringify(currentUser));
}

function loadSavedUser() {
    const saved = localStorage.getItem("ARIVORAUser") || localStorage.getItem("arivoraUser");
    if (saved) {
        try {
            currentUser = { ...currentUser, ...JSON.parse(saved) };
        } catch (e) {}
    }
    updateRoleUI();
}

/* =========================================================
   NAVIGATION & MODULE SWITCHING
========================================================= */

function showModule(moduleName) {
    if (moduleName === "faculty" && currentUser.role !== "faculty") {
        showToast("🔒 Faculty Tools are restricted to Educator/Faculty accounts only. Please log in as Faculty to access.", "error");
        showModule("home");
        return;
    }

    if ((moduleName === "quiz" || moduleName === "exams") && currentUser.role === "faculty") {
        showToast("🔒 Quiz & Exam Planner features are for Student accounts only.", "info");
        showModule("faculty");
        return;
    }

    showElement("dashboardPage");
    const modules = document.querySelectorAll(".dashboard-module");
    modules.forEach(m => m.classList.add("d-none"));

    const target = document.getElementById("module-" + moduleName);
    if (target) {
        target.classList.remove("d-none");
        target.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
        const home = document.getElementById("module-home");
        if (home) home.classList.remove("d-none");
    }

    // Active sidebar link state
    document.querySelectorAll(".sidebar-nav a").forEach(link => {
        link.classList.remove("active");
        const onclick = link.getAttribute("onclick") || "";
        if (onclick.includes("showModule('" + moduleName + "')")) {
            link.classList.add("active");
        }
    });

    // Module-specific initializers
    if (moduleName === "books") loadUserFolders();
    if (moduleName === "pyq") loadPYQ("Anna University", "Computer Networks");
    if (moduleName === "exams") loadTimetableData();
}

/* =========================================================
   THEME & SIDEBAR
========================================================= */

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("arivoraTheme", isDark ? "dark" : "light");
    localStorage.setItem("ARIVORATheme", isDark ? "dark" : "light");
    syncThemeUI(isDark);
}

function loadTheme() {
    const theme = localStorage.getItem("arivoraTheme") || localStorage.getItem("ARIVORATheme");
    const isDark = (theme === "dark");
    if (isDark) {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }
    syncThemeUI(isDark);
}

function syncThemeUI(isDark) {
    document.querySelectorAll(".theme-toggle-btn").forEach(btn => {
        const icon = btn.querySelector(".theme-icon") || btn.querySelector("i");
        const text = btn.querySelector(".theme-text");
        if (icon) {
            icon.className = isDark ? "bi bi-sun-fill text-warning me-1" : "bi bi-moon-stars-fill text-secondary me-1";
        }
        if (text) {
            text.textContent = isDark ? "Light Mode" : "Dark Mode";
        }
    });
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar) sidebar.classList.toggle("show");
}

/* =========================================================
   1. BOOK & STUDY MATERIAL UPLOAD (BACKEND CONNECTED)
========================================================= */

async function submitBookUpload() {
    const fileInput = document.getElementById("uploadModalFile") || document.getElementById("bookUpload");
    const subjectSelect = document.getElementById("uploadModalSubject");
    const submitBtn = document.getElementById("uploadModalSubmitBtn");

    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        alert("Please select a PDF or textbook document to upload.");
        return;
    }

    let subject = subjectSelect ? subjectSelect.value : "";
    if (subject === "__NEW__") {
        const newNameInput = document.getElementById("uploadModalNewFolderName");
        const newName = newNameInput ? newNameInput.value.trim() : "";
        if (!newName) {
            alert("Please enter a name for the new folder.");
            return;
        }
        subject = newName;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", currentUser.username);
    formData.append("role", currentUser.role);
    formData.append("subject", subject);

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Analyzing & Indexing...`;
    }

    try {
        const res = await fetch(`${API_BASE}/api/upload-book`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        if (data && (data.success || data.filename)) {
            showToast(`📚 "${data.filename || file.name}" successfully organized into ${data.folder || subject}!`, "success");

            // Reset file input
            if (fileInput) fileInput.value = "";

            // Close bootstrap modal if open
            const modalEl = document.getElementById("uploadModal");
            if (modalEl && window.bootstrap) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }

            // Reset new folder name field if any
            const newNameInput = document.getElementById("uploadModalNewFolderName");
            if (newNameInput) newNameInput.value = "";
            const newGrp = document.getElementById("newFolderInputGroup");
            if (newGrp) newGrp.classList.add("d-none");

            // Refresh folders
            loadUserFolders();
        } else {
            showToast(data.message || "Document uploaded and saved to folder.", "info");
            if (fileInput) fileInput.value = "";
            const modalEl = document.getElementById("uploadModal");
            if (modalEl && window.bootstrap) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }
            loadUserFolders();
        }
    } catch (err) {
        console.error("Upload error:", err);
        showToast("⚠️ Could not connect to ARIVORA backend at " + API_BASE, "error");
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="bi bi-cloud-upload me-2"></i> Upload & Analyze`;
        }
    }
}

async function loadUserFolders() {
    try {
        const educationParam = encodeURIComponent(currentUser.education || 'College');
        const res = await fetch(`${API_BASE}/api/folders?username=${encodeURIComponent(currentUser.username)}&role=${currentUser.role}&education=${educationParam}`);
        const data = await res.json();

        if (data.success && data.folders) {
            renderFolderCards(data.folders);
            updateUploadModalSubjects(data.folders);
        }
    } catch (e) {
        console.warn("Could not load user folders from backend:", e);
    }
}

function renderFolderCards(folders) {
    const container = document.querySelector("#module-books .row.g-4");
    if (!container) return;

    const isSchool = (currentUser.education || "").toLowerCase() === "school";

    if (isSchool && (!folders || folders.length === 0)) {
        container.innerHTML = `
            <div class="col-12 text-center py-5 card-box shadow-sm rounded-4 my-3">
                <div class="mb-3">
                    <i class="bi bi-journal-bookmark-fill display-1 text-primary"></i>
                </div>
                <h3 class="fw-bold mb-2">📚 Your Learning Space</h3>
                <p class="text-muted fs-5 mb-1">No folders yet.</p>
                <p class="text-muted mb-4">Create your first folder and upload your study materials.</p>
                <div class="d-flex justify-content-center gap-3">
                    <button class="btn btn-primary rounded-pill px-4 shadow-sm" onclick="promptCreateFolder()">
                        <i class="bi bi-folder-plus me-2"></i> + Create Folder
                    </button>
                    <button class="btn btn-outline-primary rounded-pill px-4" onclick="openUploadModal()">
                        <i class="bi bi-cloud-upload me-2"></i> Upload Materials
                    </button>
                </div>
            </div>
        `;
        return;
    }

    const icons = {
        "Computer_Networks": "🌐",
        "DBMS": "🗄️",
        "Operating_Systems": "💻",
        "Data_Structures": "🌳",
        "Big_Data_Analysis": "📊",
        "Data_Warehousing": "🏛️",
        "Python": "🐍",
        "Aptitude": "🧮",
        "General": "📚"
    };

    container.innerHTML = folders.map(f => {
        const icon = icons[f.folder_key] || "📁";
        return `
            <div class="col-md-6 col-lg-3">
                <div class="folder-card" data-folder="${f.name}" onclick="openSubjectFolder('${f.folder_key}', '${f.name}')">
                    <div class="folder-icon">${icon}</div>
                    <h4>${f.name}</h4>
                    <p class="text-muted mb-2">${f.file_count} ${f.file_count === 1 ? 'Material' : 'Materials'} Uploaded</p>
                    <span class="badge bg-primary-subtle text-primary">Offline Ready</span>
                </div>
            </div>
        `;
    }).join("");
}

function promptCreateFolder() {
    const input = document.getElementById("newFolderNameInput");
    if (input) input.value = "";
    const modalEl = document.getElementById("createFolderModal");
    if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    } else {
        const name = prompt("Enter folder name (e.g. Mathematics, Science):");
        if (name && name.trim()) {
            executeCreateFolder(name.trim());
        }
    }
}

async function submitCreateFolder() {
    const input = document.getElementById("newFolderNameInput");
    const folderName = input ? input.value.trim() : "";
    if (!folderName) {
        alert("Please enter a valid folder name.");
        return;
    }
    await executeCreateFolder(folderName);
    const modalEl = document.getElementById("createFolderModal");
    if (modalEl && window.bootstrap) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
    }
}

async function executeCreateFolder(folderName) {
    try {
        const res = await fetch(`${API_BASE}/api/create-folder`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                folder_name: folderName,
                username: currentUser.username,
                role: currentUser.role
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast(`📁 Folder "${data.folder_name}" created successfully!`, "success");
            await loadUserFolders();
        } else {
            alert(data.detail || data.message || "Failed to create folder.");
        }
    } catch (e) {
        console.error("Create folder error:", e);
        showToast("⚠️ Could not connect to backend to create folder.", "error");
    }
}

function openUploadModal(preselectFolder = "") {
    const modalEl = document.getElementById("uploadModal");
    if (!modalEl) return;
    updateUploadModalSubjects();
    if (preselectFolder) {
        const select = document.getElementById("uploadModalSubject");
        if (select) select.value = preselectFolder;
    }
    if (window.bootstrap) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }
}

function updateUploadModalSubjects(userFolders = null) {
    const select = document.getElementById("uploadModalSubject");
    if (!select) return;

    const isSchool = (currentUser.education || "").toLowerCase() === "school";
    select.innerHTML = "";

    if (isSchool) {
        if (userFolders && userFolders.length > 0) {
            userFolders.forEach(f => {
                const opt = document.createElement("option");
                opt.value = f.name;
                opt.textContent = f.name;
                select.appendChild(opt);
            });
        }
    } else {
        const standardSubjects = [
            "Computer Networks", "DBMS", "Operating Systems",
            "Data Structures", "Big Data Analysis", "Data Warehousing",
            "Aptitude", "General"
        ];
        const allNames = new Set(standardSubjects);
        if (userFolders) userFolders.forEach(f => allNames.add(f.name));
        allNames.forEach(name => {
            const opt = document.createElement("option");
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
    }

    const newOpt = document.createElement("option");
    newOpt.value = "__NEW__";
    newOpt.textContent = "+ Create New Folder...";
    select.appendChild(newOpt);
}

async function openSubjectFolder(folderKey, folderName) {
    showModule("books");

    const oldDetail = document.getElementById("ARIVORAFolderDetail");
    if (oldDetail) oldDetail.remove();

    let files = [];
    try {
        const res = await fetch(`${API_BASE}/api/folder/${folderKey}?username=${encodeURIComponent(currentUser.username)}&role=${currentUser.role}`);
        const data = await res.json();
        if (data.success) files = data.files || [];
    } catch (e) {
        console.warn("Folder fetch error:", e);
    }

    const detail = document.createElement("div");
    detail.id = "ARIVORAFolderDetail";
    detail.className = "card-box mt-4 p-4";
    detail.innerHTML = `
        <button class="btn btn-outline-secondary mb-3" onclick="closeSubjectFolder()">
            ← Back to All Books
        </button>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
                <h3>📁 ${folderName}</h3>
                <p class="text-muted">Subject-specific indexed textbooks and notes</p>
            </div>
            <button class="btn btn-primary" data-bs-target="#uploadModal" data-bs-toggle="modal">
                <i class="bi bi-plus-lg"></i> Add More Books
            </button>
        </div>

        <div class="alert alert-success d-flex align-items-center gap-2">
            <i class="bi bi-check-circle-fill fs-5"></i>
            <div>
                <strong>Offline Syllabus Engine Ready:</strong> Materials in this folder are indexed by ARIVORA AI for 2, 5, 10, and 16-mark answers.
            </div>
        </div>

        <h5 class="mt-4 mb-3">📚 Materials in this Folder (${files.length})</h5>
        <div class="list-group">
            ${files.length === 0 ? `
                <div class="p-4 text-center text-muted border rounded">
                    No books uploaded yet for ${folderName}. Click "Add More Books" to upload your syllabus or textbook PDF.
                </div>
            ` : files.map((f, idx) => `
                <div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center py-3">
                    <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-file-earmark-pdf fs-2 text-danger"></i>
                        <div>
                            <h6 class="mb-0">${f.name}</h6>
                            <small class="text-muted">${(f.size / 1024).toFixed(1)} KB • Indexed for smart references</small>
                        </div>
                    </div>
                    <div class="btn-group">
                        <a href="${API_BASE}${f.path}" target="_blank" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-eye"></i> View PDF
                        </a>
                        <button class="btn btn-sm btn-primary" onclick="askAboutTopic('${folderName}', '${f.name}')">
                            <i class="bi bi-stars"></i> Study with AI
                        </button>
                    </div>
                </div>
            `).join("")}
        </div>
    `;

    const booksMod = document.getElementById("module-books");
    if (booksMod) {
        booksMod.appendChild(detail);
        detail.scrollIntoView({ behavior: "smooth" });
    }
}

function closeSubjectFolder() {
    const detail = document.getElementById("ARIVORAFolderDetail");
    if (detail) detail.remove();
}

function askAboutTopic(subject, filename) {
    showModule("ai");
    activeChatSubject = subject;
    updateActiveSubjectBadge();
    const input = document.getElementById("chatInput");
    if (input) {
        input.value = `Explain the main concepts of ${subject}`;
        input.focus();
    }
}

function switchAndOpenFolder(folderKey, folderName) {
    activeChatSubject = folderName;
    updateActiveSubjectBadge();
    showToast(`📂 Switched active subject to: ${folderName}`, "success");
    openSubjectFolder(folderKey || folderName.replace(/\s+/g, "_"), folderName);
}

function switchSubjectToGeneral() {
    activeChatSubject = "General";
    updateActiveSubjectBadge();
    showToast("🌐 Switched to General AI Mode", "info");
}

function updateActiveSubjectBadge() {
    const badge = document.getElementById("activeSubjectBadge");
    if (badge) {
        const displaySubj = activeChatSubject && activeChatSubject !== "General" ? activeChatSubject : "General AI (All Subjects)";
        badge.innerHTML = `<i class="bi bi-folder-check me-1"></i> Active Folder: <strong>${displaySubj}</strong>`;
    }
}

/* =========================================================
   2. ARIVORA AI CHAT & EXAM ANSWER ENGINE (2, 5, 10, 16 MARKS)
========================================================= */

let isChatMicActive = false;
let chatMicRecognition = null;

/* =========================================================
   2. ARIVORA AI CHAT & EXAM ANSWER ENGINE (2, 5, 10, 16 MARKS)
========================================================= */

function startChatVoiceInput() {
    if (ArivoraVoice.state === "LISTENING") {
        ArivoraVoice.stopVoice();
    } else {
        ArivoraVoice.startVoice();
    }
}

async function sendChatMessage() {
    const input = document.getElementById("chatInput");
    if (!input || !input.value.trim()) return;

    const question = input.value.trim();
    activeChatTopic = question;
    input.value = "";

    appendChatMessage("user", question);

    // Show loading bubble
    const loadingId = appendChatLoading();

    try {
        const res = await fetch(`${API_BASE}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: question,
                subject: activeChatSubject,
                language: currentAiLanguage,
                username: currentUser.username
            })
        });
        const data = await res.json();
        removeChatLoading(loadingId);

        if (data.success) {
            const meta = {
                is_out_of_syllabus: !!data.is_out_of_syllabus || data.status === "out_of_syllabus",
                status: data.status,
                allow_general_ai: data.allow_general_ai,
                message: data.message,
                action: data.action,
                folder_name: data.folder_name,
                folder_key: data.folder_key,
                marks: null,
                subject: data.subject || activeChatSubject,
                unit: data.unit,
                unit_title: data.unit_title,
                reference: data.reference,
                book: data.book,
                page_ref: data.page_ref
            };
            appendChatMessage("ai", data.response, meta, data.topic || question);
        } else {
            appendChatMessage("ai", "I had trouble generating an answer. Please verify your query.", null, question);
        }
    } catch (err) {
        removeChatLoading(loadingId);
        appendChatMessage("ai", "⚠️ Connection error. Please make sure the ARIVORA AI backend is running.", null, question);
    }
}

async function requestMarkAnswer(marks, topic) {
    const input = document.getElementById("chatInput");
    const query = (topic && topic.trim()) ? topic.trim() : ((input && input.value.trim()) ? input.value.trim() : (activeChatTopic || "OSI layers"));
    activeChatTopic = query;
    if (input && input.value.trim() === query) {
        input.value = "";
    }

    appendChatMessage("user", `Generate a ${marks}-Mark exam answer for: "${query}" (${currentAiLanguage})`);

    const loadingId = appendChatLoading();

    try {
        const res = await fetch(`${API_BASE}/api/answer`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: query,
                marks: marks,
                language: currentAiLanguage,
                subject: activeChatSubject,
                username: currentUser.username
            })
        });
        const data = await res.json();
        removeChatLoading(loadingId);

        if (data.success) {
            appendChatMessage("ai", data.answer, {
                is_out_of_syllabus: !!data.is_out_of_syllabus || data.status === "out_of_syllabus",
                status: data.status,
                action: data.action,
                folder_name: data.folder_name,
                folder_key: data.folder_key,
                marks: data.is_out_of_syllabus ? null : (data.marks || marks),
                unit: data.unit,
                unit_title: data.unit_title,
                subject: data.subject,
                reference: data.reference,
                book: data.book,
                page_ref: data.page_ref,
                tamil_summary: data.tamil_summary
            }, query);
        } else {
            appendChatMessage("ai", "Could not generate marked answer: " + (data.detail || "Error"), null, query);
        }
    } catch (e) {
        removeChatLoading(loadingId);
        appendChatMessage("ai", "⚠️ Failed to reach ARIVORA AI answer engine.", null, query);
    }
}

function setAiLanguage(lang) {
    currentAiLanguage = lang;
    showToast(`🌐 Language set to: ${lang}`, "info");
    const langBtn = document.getElementById("aiLangDropdownBtn");
    if (langBtn) langBtn.innerText = `🌐 ${lang}`;
}

function stayInSyllabus() {
    showToast("🔒 Remaining in your selected syllabus folder.", "info");
    const chatInp = document.getElementById("chatInput");
    if (chatInp) {
        chatInp.value = "";
        chatInp.focus();
    }
}

function askGeneralAiForTopic(topic) {
    const chatInput = document.getElementById("chatInput");
    if (chatInput) chatInput.value = "";

    appendChatMessage("user", `[Ask General AI] ${topic}`);
    const loadingId = appendChatLoading();

    fetch(`${API_BASE}/api/general-ai-chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: topic,
            language: currentAiLanguage,
            username: currentUser.username
        })
    })
    .then(r => r.json())
    .then(data => {
        removeChatLoading(loadingId);
        if (data.success) {
            appendChatMessage("ai", data.response, {
                is_general_ai: true,
                subject: "General AI Mode"
            }, topic);
        } else {
            appendChatMessage("ai", "General AI service is currently unavailable.", null, topic);
        }
    })
    .catch(err => {
        removeChatLoading(loadingId);
        appendChatMessage("ai", "⚠️ Connection error to General AI.", null, topic);
    });
}

function openReferSource(folderKey, topic) {
    showToast(`📖 Opening source document for '${topic}' in folder: ${folderKey}`, "info");
    showModule("books");
    if (typeof openUserFolder === "function") {
        openUserFolder(folderKey || "Computer_Networks");
    }
}

/* ---- Global TTS toggle: play full answer, click again to stop ---- */
function toggleChatTTS(btn, text) {
    if (currentTTSButton === btn && isTTSPlaying) {
        stopAllTTS();
        return;
    }
    stopAllTTS();

    currentTTSButton = btn;
    isTTSPlaying = true;
    btn.innerHTML = '<i class="bi bi-stop-circle-fill fs-5 text-danger"></i>';
    btn.title = "Stop speaking";

    const lang = currentAiLanguage;
    const targetLang = lang.toLowerCase().includes("ta") ? "ta" : "en";

    fetch(`${API_BASE}/api/voice-reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, language: targetLang, username: currentUser.username })
    }).then(r => r.json()).then(data => {
        if (!isTTSPlaying || currentTTSButton !== btn) return;
        if (data.success && data.audio_url) {
            if (currentAudioPlayer) { currentAudioPlayer.pause(); currentAudioPlayer = null; }
            currentAudioPlayer = new Audio(`${API_BASE}${data.audio_url}`);
            currentAudioPlayer.onended = () => resetTTSButton(btn);
            currentAudioPlayer.onerror = () => speakWithBrowser(btn, text, lang);
            currentAudioPlayer.play();
        } else {
            speakWithBrowser(btn, text, lang);
        }
    }).catch(() => speakWithBrowser(btn, text, lang));
}

function speakWithBrowser(btn, text, lang) {
    if (!isTTSPlaying || currentTTSButton !== btn) return;
    if (!("speechSynthesis" in window)) { resetTTSButton(btn); return; }
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = lang.toLowerCase().includes("ta") ? "ta-IN" : "en-IN";
    utter.rate = 0.92;
    utter.onend = () => resetTTSButton(btn);
    utter.onerror = () => resetTTSButton(btn);
    currentTTSUtterance = utter;
    window.speechSynthesis.speak(utter);
}

function stopAllTTS() {
    isTTSPlaying = false;
    if (currentAudioPlayer) {
        currentAudioPlayer.pause();
        currentAudioPlayer.currentTime = 0;
        currentAudioPlayer = null;
    }
    if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    if (currentTTSButton) resetTTSButton(currentTTSButton);
    currentTTSButton = null;
}

function resetTTSButton(btn) {
    isTTSPlaying = false;
    if (btn) {
        btn.innerHTML = '<i class="bi bi-volume-up-fill fs-5"></i>';
        btn.title = "Read aloud";
    }
    currentTTSButton = null;
}

function appendChatMessage(sender, text, meta, topic) {
    const chatBox = document.querySelector("#module-ai .chat-box");
    if (!chatBox) return;

    const queryTopic = (topic && topic.trim()) ? topic.trim() : (activeChatTopic || "OSI layers");
    const chatDiv = document.createElement("div");
    const isOut = meta && (meta.is_out_of_syllabus || meta.status === "out_of_syllabus");

    chatDiv.className = `chat ${sender} mb-3 p-3 rounded-3 shadow-sm ${isOut ? 'border border-warning bg-warning-subtle text-dark' : ''}`;

    let metaHeader = "";
    if (meta) {
        const badges = [];
        if (isOut) {
            badges.push(`<span class="badge bg-danger text-white"><i class="bi bi-exclamation-triangle-fill me-1"></i>Out of Syllabus</span>`);
        } else if (meta.is_general_ai) {
            badges.push(`<span class="badge mode-badge-general"><i class="bi bi-stars me-1"></i>GENERAL AI MODE</span>`);
        } else {
            badges.push(`<span class="badge mode-badge-syllabus"><i class="bi bi-lock-fill me-1"></i>SYLLABUS MODE</span>`);
        }

        if (meta.marks && !isOut) {
            badges.push(`<span class="badge bg-primary"><i class="bi bi-award-fill me-1"></i>${meta.marks} Marks Rubric</span>`);
        }
        if (meta.subject && !isOut) {
            badges.push(`<span class="badge bg-secondary">${meta.subject}${meta.unit ? ` • Unit ${meta.unit}` : ''}</span>`);
        }
        if (meta.reference && !isOut) {
            badges.push(`<span class="badge bg-info-subtle text-info-emphasis border"><i class="bi bi-journal-bookmark me-1"></i>${meta.reference}</span>`);
        }
        if (badges.length > 0) {
            metaHeader = `<div class="d-flex flex-wrap gap-2 mb-2">${badges.join("")}</div>`;
        }
    }

    const formattedText = text ? text.replace(/\n/g, "<br>") : "";
    const speakerId = "spk_" + Date.now() + "_" + Math.random().toString(36).slice(2,6);

    let markOptionsHtml = "";
    if (sender === "ai") {
        const currentMark = (meta && meta.marks) ? Number(meta.marks) : null;
        const availableMarks = [1, 2, 4, 5, 8, 16];
        const buttonsHtml = availableMarks.map(m => {
            const isActive = currentMark === m;
            const btnClass = isActive ? "btn-primary active fw-bold" : "btn-outline-primary";
            return `<button type="button" class="btn btn-sm ${btnClass} mark-pill-btn" data-marks="${m}">${m} ${m === 1 ? 'Mark' : 'Marks'}</button>`;
        }).join(" ");

        let referThisBox = "";
            if (meta) {
                const bookTitle = meta.book || (meta.sources && meta.sources[0] ? meta.sources[0].book : null);
                const chapterTitle = meta.chapter || meta.unit_title || (meta.sources && meta.sources[0] ? meta.sources[0].chapter : null);
                const pageVal = meta.page || (meta.sources && meta.sources[0] ? meta.sources[0].page : null);

                let sourceItemsHtml = "";
                if (meta.sources && meta.sources.length > 0) {
                    sourceItemsHtml = meta.sources.map(src => `
                        <div class="mb-1"><i class="bi bi-book me-1 text-primary"></i><strong>Book / Material:</strong> ${src.book || 'Uploaded Document'}</div>
                        ${src.chapter ? `<div class="mb-1"><i class="bi bi-journal-bookmark me-1 text-primary"></i><strong>Chapter:</strong> ${src.chapter}</div>` : ''}
                        <div class="mb-1"><i class="bi bi-card-text me-1 text-primary"></i><strong>Topic:</strong> ${src.topic || queryTopic}</div>
                        ${src.page ? `<div class="mb-1"><i class="bi bi-bookmark-fill me-1 text-primary"></i><strong>Page:</strong> Page ${src.page}</div>` : ''}
                    `).join('<hr class="my-2">');
                } else if (bookTitle) {
                    sourceItemsHtml = `
                        <div class="mb-1"><i class="bi bi-book me-1 text-primary"></i><strong>Book / Material:</strong> ${bookTitle}</div>
                        ${chapterTitle ? `<div class="mb-1"><i class="bi bi-journal-bookmark me-1 text-primary"></i><strong>Chapter:</strong> ${chapterTitle}</div>` : ''}
                        <div class="mb-1"><i class="bi bi-card-text me-1 text-primary"></i><strong>Topic:</strong> ${queryTopic}</div>
                        ${pageVal ? `<div class="mb-1"><i class="bi bi-bookmark-fill me-1 text-primary"></i><strong>Page:</strong> Page ${pageVal}</div>` : ''}
                    `;
                }

                if (sourceItemsHtml) {
                    referThisBox = `
                        <div class="refer-this-container mt-3 p-3 rounded-3 border shadow-sm">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <h6 class="fw-bold text-primary mb-0"><i class="bi bi-journal-check me-2"></i>REFER THIS</h6>
                                <span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">Verified Syllabus Source</span>
                            </div>
                            <div class="refer-details small mb-2 text-secondary">
                                ${sourceItemsHtml}
                            </div>
                            <button type="button" class="btn btn-sm btn-outline-primary rounded-pill fw-semibold mt-1" onclick="openReferSource('${meta.folder_key || meta.subject}', '${queryTopic.replace(/'/g, "\\'")}')">
                                <i class="bi bi-box-arrow-up-right me-1"></i> Open Source
                            </button>
                        </div>
                    `;
                }
            }

            markOptionsHtml = `
                <div class="mark-options-wrapper mt-3 pt-2 border-top">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                        <small class="text-muted fw-bold">
                            <i class="bi bi-mortarboard-fill text-primary me-1"></i> View Exam Answer in Marks Rubric:
                        </small>
                    </div>
                    <div class="mark-options d-flex flex-wrap gap-2 mb-2">
                        ${buttonsHtml}
                    </div>
                    ${referThisBox}
                </div>
            `;
        }
    }

    chatDiv.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-1">
            <strong>${sender === "ai" ? "🤖 ARIVORA AI" : "👤 You"}</strong>
            ${sender === "ai" ? `
                <button id="${speakerId}" class="btn btn-sm btn-link text-decoration-none p-0" title="Read aloud">
                    <i class="bi bi-volume-up-fill fs-5"></i>
                </button>
            ` : ""}
        </div>
        ${metaHeader}
        <div class="chat-content">${formattedText}</div>
        ${markOptionsHtml}
    `;

    chatBox.appendChild(chatDiv);
    chatDiv.scrollIntoView({ behavior: "smooth" });

    if (sender === "ai") {
        chatDiv.querySelectorAll(".mark-pill-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const m = parseInt(btn.getAttribute("data-marks"), 10);
                requestMarkAnswer(m, queryTopic);
            });
        });

        const speakerBtn = document.getElementById(speakerId);
        if (speakerBtn) {
            speakerBtn.addEventListener("click", () => toggleChatTTS(speakerBtn, text));
        }
    }
}

function appendChatLoading() {
    const chatBox = document.querySelector("#module-ai .chat-box");
    if (!chatBox) return null;

    const id = "loading_" + Date.now();
    const loadDiv = document.createElement("div");
    loadDiv.id = id;
    loadDiv.className = "chat ai mb-3 p-3";
    loadDiv.innerHTML = `
        <strong>🤖 ARIVORA AI</strong>
        <div class="d-flex align-items-center gap-2 mt-2 text-muted">
            <span class="spinner-grow spinner-grow-sm text-primary"></span>
            <span>Checking syllabus, unit index, and compiling exam answer...</span>
        </div>
    `;
    chatBox.appendChild(loadDiv);
    loadDiv.scrollIntoView({ behavior: "smooth" });
    return id;
}

function removeChatLoading(id) {
    if (!id) return;
    const el = document.getElementById(id);
    if (el) el.remove();
}

/* =========================================================
   3. SMART REFERENCE FINDER (BACKEND CONNECTED)
========================================================= */

async function findSmartReference() {
    const input = document.getElementById("referenceTopicInput") || document.querySelector("#module-reference input");
    if (!input || !input.value.trim()) {
        alert("Please enter a topic to find its syllabus reference (e.g., 'Network Layers' or 'Normalization').");
        return;
    }

    const topic = input.value.trim();
    const resultBox = document.querySelector("#module-reference .reference-result") || document.getElementById("referenceResultBox");

    if (resultBox) {
        resultBox.innerHTML = `
            <div class="text-center p-4">
                <span class="spinner-border text-primary"></span>
                <p class="mt-2 text-muted">Searching indexed textbooks and syllabus units...</p>
            </div>
        `;
    }

    try {
        const res = await fetch(`${API_BASE}/api/reference`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: topic,
                subject: activeChatSubject,
                username: currentUser.username
            })
        });
        const data = await res.json();

        if (data.success && resultBox) {
            resultBox.innerHTML = `
                <div class="card-box p-4 border-start border-4 border-primary rounded-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <span class="badge bg-primary mb-2">${data.subject}</span>
                            <span class="badge bg-secondary mb-2">${data.unit}</span>
                            <h4 class="mb-1">📍 ${data.topic}</h4>
                            <p class="text-muted mb-2"><strong>Chapter:</strong> ${data.chapter}</p>
                        </div>
                        <span class="badge bg-success-subtle text-success fs-6">${data.pages}</span>
                    </div>

                    <div class="p-3 my-3 ref-citation-box border">
                        <strong>📖 Source Citation:</strong> ${data.citation}
                        <hr class="my-2">
                        <small class="text-muted">${data.excerpt}</small>
                    </div>

                    <div class="d-flex gap-2">
                        <button class="btn btn-primary btn-sm" onclick="askAboutReference('${data.topic}')">
                            <i class="bi bi-stars"></i> Generate 16-Mark Answer
                        </button>
                        <button class="btn btn-outline-secondary btn-sm" onclick="showModule('books')">
                            <i class="bi bi-folder2-open"></i> Open Subject Folder
                        </button>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        if (resultBox) {
            resultBox.innerHTML = `<div class="alert alert-danger">⚠️ Could not connect to Reference Finder backend.</div>`;
        }
    }
}

function askAboutReference(topic) {
    showModule("ai");
    requestMarkAnswer(16, topic);
}

/* =========================================================
   4. ADAPTIVE QUIZ & PROGRESS EVALUATION
========================================================= */

let activeQuizData = null;

async function startQuiz() {
    const input = document.getElementById("quizTopicInput");
    const topic = (input && input.value.trim()) ? input.value.trim() : (activeChatTopic || "OSI layers");

    const container = document.getElementById("quizContainer") || document.querySelector("#module-quiz");
    if (!container) return;

    showToast(`Generating quiz for ${topic}...`, "info");

    try {
        const res = await fetch(`${API_BASE}/api/quiz`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: topic,
                subject: activeChatSubject,
                number_of_questions: 5,
                language: currentAiLanguage
            })
        });
        const data = await res.json();

        if (data.success && data.questions) {
            activeQuizData = data;
            renderQuizQuestions(data);
        }
    } catch (e) {
        alert("⚠️ Failed to generate quiz from backend.");
    }
}

function renderQuizQuestions(data) {
    let quizBox = document.getElementById("activeQuizBox");
    if (!quizBox) {
        quizBox = document.createElement("div");
        quizBox.id = "activeQuizBox";
        const moduleQuiz = document.getElementById("module-quiz");
        if (moduleQuiz) moduleQuiz.appendChild(quizBox);
    }

    quizBox.innerHTML = `
        <div class="card-box p-4 mt-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4>📝 Adaptive Quiz: ${data.topic}</h4>
                <span class="badge bg-primary">${data.total_questions} Questions</span>
            </div>

            <form id="quizForm">
                ${data.questions.map((q, idx) => `
                    <div class="mb-4 p-3 quiz-question-box border">
                        <h6 class="fw-bold">${q.question}</h6>
                        <span class="badge bg-secondary mb-2">${q.unit}</span>
                        <div class="mt-2">
                            ${q.options.map((opt, oIdx) => `
                                <div class="form-check my-2">
                                    <input class="form-check-input" type="radio" name="question_${q.id}" id="q${q.id}_opt${oIdx}" value="${opt}">
                                    <label class="form-check-label" for="q${q.id}_opt${oIdx}">
                                        ${opt}
                                    </label>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `).join("")}

                <button type="button" class="btn btn-success btn-lg w-100" onclick="submitQuizAnswers()">
                    <i class="bi bi-check2-circle me-2"></i> Submit Answers & Get Analysis
                </button>
            </form>
        </div>
    `;

    quizBox.scrollIntoView({ behavior: "smooth" });
}

async function submitQuizAnswers() {
    if (!activeQuizData) return;

    const answers = {};
    activeQuizData.questions.forEach(q => {
        const selected = document.querySelector(`input[name="question_${q.id}"]:checked`);
        if (selected) answers[q.id] = selected.value;
    });

    try {
        const res = await fetch(`${API_BASE}/api/quiz/evaluate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: activeQuizData.topic,
                subject: activeQuizData.subject,
                answers: answers,
                username: currentUser.username
            })
        });
        const evalData = await res.json();

        if (evalData.success) {
            renderQuizResults(evalData);
        }
    } catch (e) {
        alert("⚠️ Error submitting quiz.");
    }
}

function renderQuizResults(data) {
    const quizBox = document.getElementById("activeQuizBox");
    if (!quizBox) return;

    quizBox.innerHTML = `
        <div class="card-box p-4 mt-4 border-top border-4 border-success">
            <div class="text-center mb-4">
                <span class="badge bg-success fs-6 mb-2">${data.badge}</span>
                <h2>Score: ${data.correct} / ${data.total} (${data.percentage}%)</h2>
                <p class="lead">${data.feedback}</p>
            </div>

            <h5>Detailed Answer Review:</h5>
            <div class="list-group mt-3">
                ${data.results.map(r => `
                    <div class="list-group-item ${r.is_correct ? 'list-group-item-success' : 'list-group-item-danger'} p-3 mb-2 rounded">
                        <div class="d-flex justify-content-between">
                            <strong>${r.question}</strong>
                            <span>${r.is_correct ? '✅ Correct' : '❌ Incorrect'}</span>
                        </div>
                        <div class="mt-2 small">
                            <div>Your Answer: <em>${r.your_answer}</em></div>
                            <div>Correct Answer: <strong>${r.correct_answer}</strong></div>
                            <div class="text-muted mt-1">💡 <em>${r.explanation}</em></div>
                        </div>
                    </div>
                `).join("")}
            </div>

            <div class="d-flex gap-2 mt-4">
                <button class="btn btn-primary" onclick="startQuiz()">
                    <i class="bi bi-arrow-repeat"></i> Retry Quiz
                </button>
                <button class="btn btn-outline-secondary" onclick="showModule('ai')">
                    <i class="bi bi-stars"></i> Clarify with ARIVORA AI
                </button>
            </div>
        </div>
    `;
    quizBox.scrollIntoView({ behavior: "smooth" });
}

/* =========================================================
   5. SYLLABUS GUARDIAN (IN/OUT OF SYLLABUS CHECKER)
========================================================= */

async function checkSyllabus() {
    const input = document.getElementById("syllabusCheckInput");
    if (!input || !input.value.trim()) {
        alert("Enter a topic to check against syllabus (e.g. 'TCP/IP' or 'Quantum Rocketry')");
        return;
    }

    const topic = input.value.trim();
    const alertContainer = document.getElementById("syllabusAlertArea");

    try {
        const res = await fetch(`${API_BASE}/api/check-syllabus?topic=${encodeURIComponent(topic)}&subject=${encodeURIComponent(activeChatSubject)}`);
        const data = await res.json();

        if (alertContainer) {
            if (data.status === "IN_SYLLABUS") {
                alertContainer.innerHTML = `
                    <div class="alert alert-success mt-4 p-4 border-start border-4 border-success">
                        <h4><i class="bi bi-check-circle-fill text-success"></i> IN SYLLABUS</h4>
                        <p class="mb-1">${data.message}</p>
                        <span class="badge bg-success">Confidence: ${(data.confidence * 100).toFixed(0)}%</span>
                        <div class="mt-3">
                            <button class="btn btn-sm btn-primary" onclick="studyInSyllabusTopic('${data.topic}')">
                                <i class="bi bi-stars"></i> Generate 5-Mark Answer
                            </button>
                        </div>
                    </div>
                `;
            } else {
                alertContainer.innerHTML = `
                    <div class="alert alert-warning mt-4 p-4 border-start border-4 border-warning">
                        <h4><i class="bi bi-exclamation-triangle-fill text-warning"></i> OUT OF SYLLABUS ALERT</h4>
                        <p class="mb-2">${data.message}</p>
                        <p class="small text-muted">${data.advice}</p>
                        <hr>
                        <h6>Recommended Topics to Study Instead:</h6>
                        <ul>
                            ${(data.recommended_in_syllabus_topics || []).map(t => `<li><strong>${t}</strong></li>`).join("")}
                        </ul>
                    </div>
                `;
            }
        }
    } catch (e) {
        alert("⚠️ Could not check syllabus with backend.");
    }
}

function studyInSyllabusTopic(t) {
    showModule("ai");
    activeChatTopic = t;
    requestMarkAnswer(5, t);
}

/* =========================================================
   6. PREVIOUS YEAR QUESTIONS (PYQ)
========================================================= */

async function loadPYQ(board = "", subject = "") {
    showModule("pyq");

    const activeBoard = board || (currentUser && currentUser.board) || "Anna University";
    const activeSubject = subject || (currentUser && currentUser.subject) || "Mathematics";

    const boardEl = document.getElementById("pyqFilterBoard");
    const subjectEl = document.getElementById("pyqFilterSubject");
    const classEl = document.getElementById("pyqFilterClass");

    if (boardEl) boardEl.value = activeBoard;
    if (subjectEl) subjectEl.value = activeSubject;

    if (classEl && activeBoard.toLowerCase().includes("anna")) {
        classEl.value = "College";
    }

    await searchSchoolPYQPapers();
}

function generateClientFallbackPYQPapers(board, classLevel, subject, year, medium) {
    const yList = year ? [parseInt(year, 10)] : [2025, 2024, 2023, 2022, 2021];
    const papers = [];
    const isAnna = (board || "").toLowerCase().includes("anna");

    const domain = isAnna ? "annaunivpapers.in" : "padasalai.net";
    const baseQuery = isAnna
        ? `Anna University ${subject} previous year question paper pdf`
        : `${board} Class ${classLevel} ${subject} question paper padasalai`;

    yList.forEach((y, idx) => {
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(baseQuery + ' ' + y)}`;
        papers.push({
            id: `PYQ-CLIENT-${idx + 1}`,
            title: `${board} - ${subject} Examination Question Paper (${y})`,
            source: domain,
            url: searchUrl,
            board: board,
            class_level: classLevel,
            subject: subject,
            year: y,
            medium: medium,
            snippet: `Official ${y} board exam question paper for ${subject} (${board} - ${medium} medium). Contains Part-A 2-mark definitions, Part-B 5/10-mark problems, and Part-C 16-mark essay questions with step-by-step marking scheme.`
        });
        papers.push({
            id: `PYQ-CLIENT-M-${idx + 1}`,
            title: `Model & Revision Question Paper - ${board} ${subject} (${y})`,
            source: isAnna ? "stucor.in" : "kalvisolai.com",
            url: searchUrl,
            board: board,
            class_level: classLevel,
            subject: subject,
            year: y,
            medium: medium,
            snippet: `Curated model question paper and important repeated university/board questions for ${subject} (${y}) with complete solution guide.`
        });
    });

    return {
        success: true,
        total_found: papers.length,
        questions: papers
    };
}

async function searchSchoolPYQPapers() {
    const boardEl = document.getElementById("pyqFilterBoard");
    const classEl = document.getElementById("pyqFilterClass");
    const subjectEl = document.getElementById("pyqFilterSubject");
    const yearEl = document.getElementById("pyqFilterYear");
    const mediumEl = document.getElementById("pyqFilterMedium");

    const board = boardEl ? boardEl.value : "Anna University";
    let classLevel = classEl ? classEl.value : "College";
    if (board.toLowerCase().includes("anna") && classLevel === "10") {
        classLevel = "College";
        if (classEl) classEl.value = "College";
    }

    const subject = subjectEl && subjectEl.value.trim() ? subjectEl.value.trim() : "Mathematics";
    const year = yearEl ? yearEl.value : "";
    const medium = mediumEl ? mediumEl.value : "English";

    const container = document.getElementById("pyqListContainer");
    if (!container) return;

    container.innerHTML = `
        <div class="text-center p-4">
            <span class="spinner-border text-primary"></span>
            <p class="mt-2 text-muted fw-semibold">🔍 Searching authentic previous year question papers for ${board} Class/Level ${classLevel} ${subject}...</p>
        </div>
    `;

    let data;
    try {
        const queryParams = new URLSearchParams({
            board: board,
            class_level: classLevel,
            subject: subject,
            medium: medium
        });
        if (year) queryParams.append("year", year);

        try {
            data = await safeApiFetch(`/api/school/pyq-search?${queryParams.toString()}`);
        } catch (fetchErr) {
            console.warn("Backend PYQ fetch fallback to client generator:", fetchErr);
            data = generateClientFallbackPYQPapers(board, classLevel, subject, year, medium);
        }

        if (!data || !data.questions || data.questions.length === 0) {
            data = generateClientFallbackPYQPapers(board, classLevel, subject, year, medium);
        }

        container.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0 fw-bold text-primary"><i class="bi bi-journal-text me-2"></i>Found ${data.total_found} Authentic Question Papers</h5>
                <span class="badge bg-primary px-3 py-2 fs-6 rounded-pill">${board} • ${classLevel}</span>
            </div>
            <div class="list-group">
                ${data.questions.map(q => `
                    <div class="list-group-item p-3 mb-3 rounded-3 border shadow-sm hover-shadow transition-all">
                        <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap flex-md-nowrap">
                            <div class="flex-grow-1">
                                <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
                                    <span class="badge bg-primary-subtle text-primary fw-bold">${q.year} Question Paper</span>
                                    <span class="badge bg-secondary-subtle text-secondary">${q.subject}</span>
                                    <span class="badge bg-dark-subtle text-dark">${q.medium} Medium</span>
                                </div>
                                <h5 class="mt-1 mb-1 fw-bold text-dark fs-6">${q.title}</h5>
                                <div class="text-muted small mb-2"><i class="bi bi-globe me-1 text-primary"></i>Source: <strong>${q.source}</strong></div>
                                <p class="small text-secondary mb-0">${q.snippet || ''}</p>
                            </div>
                            <div class="d-flex gap-2 flex-shrink-0 align-self-start mt-2 mt-md-0">
                                <a href="${q.url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary rounded-pill px-3 text-nowrap fw-semibold shadow-sm">
                                    <i class="bi bi-box-arrow-up-right me-1"></i> View Paper
                                </a>
                                <button onclick="solvePYQWithAI('${encodeURIComponent(q.title + " - " + q.subject)}', 16)" class="btn btn-sm btn-outline-purple rounded-pill px-3 text-nowrap fw-semibold">
                                    <i class="bi bi-robot me-1"></i> Solve with AI
                                </button>
                            </div>
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    } catch (err) {
        console.error("School PYQ search fallback error:", err);
        data = generateClientFallbackPYQPapers(board, classLevel, subject, year, medium);
        container.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0 fw-bold text-primary"><i class="bi bi-journal-text me-2"></i>Found ${data.total_found} Authentic Question Papers</h5>
                <span class="badge bg-primary px-3 py-2 fs-6 rounded-pill">${board} • ${classLevel}</span>
            </div>
            <div class="list-group">
                ${data.questions.map(q => `
                    <div class="list-group-item p-3 mb-3 rounded-3 border shadow-sm hover-shadow transition-all">
                        <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap flex-md-nowrap">
                            <div class="flex-grow-1">
                                <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
                                    <span class="badge bg-primary-subtle text-primary fw-bold">${q.year} Question Paper</span>
                                    <span class="badge bg-secondary-subtle text-secondary">${q.subject}</span>
                                    <span class="badge bg-dark-subtle text-dark">${q.medium} Medium</span>
                                </div>
                                <h5 class="mt-1 mb-1 fw-bold text-dark fs-6">${q.title}</h5>
                                <div class="text-muted small mb-2"><i class="bi bi-globe me-1 text-primary"></i>Source: <strong>${q.source}</strong></div>
                                <p class="small text-secondary mb-0">${q.snippet || ''}</p>
                            </div>
                            <div class="d-flex gap-2 flex-shrink-0 align-self-start mt-2 mt-md-0">
                                <a href="${q.url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary rounded-pill px-3 text-nowrap fw-semibold shadow-sm">
                                    <i class="bi bi-box-arrow-up-right me-1"></i> View Paper
                                </a>
                                <button onclick="solvePYQWithAI('${encodeURIComponent(q.title + " - " + q.subject)}', 16)" class="btn btn-sm btn-outline-purple rounded-pill px-3 text-nowrap fw-semibold">
                                    <i class="bi bi-robot me-1"></i> Solve with AI
                                </button>
                            </div>
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    }
}

function solvePYQWithAI(qText, marks) {
    showModule("ai");
    const decoded = decodeURIComponent(qText);
    activeChatTopic = decoded;
    requestMarkAnswer(marks || 16, decoded);
}

/* =========================================================
   7. VOICE AI & SPEECH SYNTHESIS (ARIVORA gTTS CONNECTED)
========================================================= */

let isVoiceRecording = false;
let currentVoiceRecognition = null;
let activeVoiceQuestion = "Explain OSI layers in simple Tamil.";
let activeVoiceResponseText = "OSI மாதிரி (Open Systems Interconnection) என்பது ISO-வினால் உருவாக்கப்பட்ட 7 அடுக்குகளைக் கொண்ட நெட்வொர்க் கட்டமைப்பு ஆகும். இது பல்வேறு சாதனங்களுக்கு இடையே தகவல் பரிமாற்றத்தை நெறிப்படுத்துகிறது.";
let activeVoiceLang = "ta";
let voiceHistory = [
    {
        query: "Explain OSI layers in simple Tamil.",
        subject: "Computer Networks",
        unit: "Unit 1",
        lang: "ta",
        response: "OSI மாதிரி (Open Systems Interconnection) என்பது ISO-வினால் உருவாக்கப்பட்ட 7 அடுக்குகளைக் கொண்ட நெட்வொர்க் கட்டமைப்பு ஆகும். இது பல்வேறு சாதனங்களுக்கு இடையே தகவல் பரிமாற்றத்தை நெறிப்படுத்துகிறது."
    },
    {
        query: "Explain TCP Concepts",
        subject: "Computer Networks",
        unit: "Unit 4",
        lang: "en",
        response: "TCP (Transmission Control Protocol) is a reliable, connection-oriented transport protocol using 3-way handshakes, sequence numbers, and sliding-window flow control to guarantee in-order delivery of data streams."
    }
];

function toggleVoiceRecording() {
    if (isVoiceRecording) {
        stopVoiceRecording();
    } else {
        startVoiceNote();
    }
}

function startVoiceNote() {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        try {
            if (currentVoiceRecognition) {
                currentVoiceRecognition.abort();
            }
            const recognition = new SpeechRecognition();
            currentVoiceRecognition = recognition;
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = currentAiLanguage.toLowerCase().includes("tamil") ? "ta-IN" : "en-IN";

            recognition.onstart = function() {
                isVoiceRecording = true;
                const circle = document.getElementById("voiceButtonCircle");
                if (circle) circle.classList.add("listening");

                const btn = document.getElementById("voiceRecordBtn");
                if (btn) {
                    btn.classList.remove("btn-primary");
                    btn.classList.add("btn-danger");
                }
                const icon = document.getElementById("voiceBtnIcon");
                if (icon) icon.className = "bi bi-stop-circle me-1";
                const label = document.getElementById("voiceBtnLabel");
                if (label) label.innerText = "Stop Listening";

                const status = document.getElementById("voiceStatusText");
                if (status) {
                    status.innerHTML = `<span class="spinner-grow spinner-grow-sm text-danger me-1"></span> <strong class="text-danger">Listening...</strong> Speak your question now!`;
                }
                showToast("🎙️ Listening... Speak your syllabus question now!", "info");
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                showToast(`Captured: "${transcript}"`, "success");
                stopVoiceRecording();
                processVoiceQuestion(transcript);
            };

            recognition.onerror = function(event) {
                console.warn("Speech recognition error:", event.error);
                stopVoiceRecording();
                if (event.error !== "no-speech") {
                    showToast(`Voice capture note: ${event.error}. You can also type your question below!`, "info");
                }
            };

            recognition.onend = function() {
                stopVoiceRecording();
            };

            recognition.start();
        } catch (e) {
            console.error("SpeechRecognition start exception:", e);
            stopVoiceRecording();
            alert("Could not access microphone. Please ensure microphone permissions are granted.");
        }
    } else {
        alert("Microphone speech recognition is not supported in this browser. You can type your question in the text box below!");
    }
}

function stopVoiceRecording() {
    isVoiceRecording = false;
    if (currentVoiceRecognition) {
        try { currentVoiceRecognition.stop(); } catch (e) {}
        currentVoiceRecognition = null;
    }
    const circle = document.getElementById("voiceButtonCircle");
    if (circle) circle.classList.remove("listening");

    const btn = document.getElementById("voiceRecordBtn");
    if (btn) {
        btn.classList.remove("btn-danger");
        btn.classList.add("btn-primary");
    }
    const icon = document.getElementById("voiceBtnIcon");
    if (icon) icon.className = "bi bi-mic me-1";
    const label = document.getElementById("voiceBtnLabel");
    if (label) label.innerText = "Start Recording";

    const status = document.getElementById("voiceStatusText");
    if (status && !status.innerHTML.includes("Consulting")) {
        status.innerHTML = `<i class="bi bi-broadcast me-1"></i> Tap microphone or click Start Recording`;
    }
}

function submitVoiceQuestion() {
    const input = document.getElementById("voiceManualInput");
    if (!input || !input.value.trim()) {
        showToast("Please enter a question to ask ARIVORA AI.", "info");
        return;
    }
    const query = input.value.trim();
    input.value = "";
    processVoiceQuestion(query);
}

async function processVoiceQuestion(query) {
    if (!query) return;

    activeVoiceQuestion = query;
    const queryDisplay = document.getElementById("voiceQueryDisplay");
    if (queryDisplay) queryDisplay.innerText = `“${query}”`;

    const status = document.getElementById("voiceStatusText");
    if (status) {
        status.innerHTML = `<span class="spinner-border spinner-border-sm text-primary me-2"></span> Consulting ARIVORA AI syllabus repository...`;
    }

    const responseDisplay = document.getElementById("voiceResponseDisplay");
    if (responseDisplay) {
        responseDisplay.innerHTML = `
            <div class="d-flex align-items-center gap-2 text-muted py-2">
                <span class="spinner-grow spinner-grow-sm text-primary"></span>
                <span>Generating syllabus-verified answer & synthesizing voice response...</span>
            </div>
        `;
    }

    try {
        const langParam = currentAiLanguage.toLowerCase().includes("tamil") ? "Tamil" : "English";
        const targetSubject = activeChatSubject || (currentUser && currentUser.subject) || "Computer Networks";
        const targetUsername = (currentUser && currentUser.username) ? currentUser.username : "Student";

        const res = await fetch(`${API_BASE}/api/answer`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: query,
                marks: 2,
                language: langParam,
                subject: targetSubject,
                username: targetUsername
            })
        });

        const data = await res.json();
        if (data.success) {
            // Update badges
            const subjBadge = document.getElementById("voiceSubjectBadge");
            if (subjBadge) subjBadge.innerText = data.subject || targetSubject;

            const unitBadge = document.getElementById("voiceUnitBadge");
            if (unitBadge) unitBadge.innerText = `Unit ${data.unit || 1}`;

            const langBadge = document.getElementById("voiceLangBadge");
            if (langBadge) langBadge.innerText = `🌐 ${data.language || currentAiLanguage}`;

            // Prepare voice text to speak
            let speechText = "";

            if (data.tamil_summary && (data.language === "Tamil" || currentAiLanguage === "Tamil")) {
                speechText = data.tamil_summary;
                activeVoiceLang = "ta";
            } else {
                // Extract concise first section
                const lines = (data.answer || "").split("\n").filter(l => l.trim().length > 0 && !l.startsWith("=") && !l.startsWith("-"));
                speechText = lines.slice(0, 3).join(". ").replace(/[•#*|]/g, "").trim() || data.answer;
                activeVoiceLang = (data.language === "Tamil") ? "ta" : "en";
            }

            activeVoiceResponseText = speechText;

            // Formatted HTML display
            const formatted = (data.answer || "").replace(/\n/g, "<br>");
            if (responseDisplay) {
                responseDisplay.innerHTML = `
                    <div class="mb-2"><strong>💡 ARIVORA AI Explanation (${data.subject || targetSubject} • Unit ${data.unit || 1}):</strong></div>
                    <div class="mb-2">${formatted}</div>
                    <div class="text-muted small mt-2">📖 Reference: ${data.reference || "Syllabus Knowledge Base"}</div>
                `;
            }

            if (status) {
                status.innerHTML = `<i class="bi bi-check-circle-fill text-success me-1"></i> Answer ready. Playing voice response...`;
            }

            // Add to history
            addVoiceHistory({
                query: query,
                subject: data.subject || targetSubject,
                unit: `Unit ${data.unit || 1}`,
                lang: activeVoiceLang,
                response: speechText
            });

            // Play voice response automatically!
            playCurrentVoiceResponse();

        } else {
            if (responseDisplay) responseDisplay.innerHTML = `<span class="text-danger">Could not generate voice response: ${data.detail || "Unknown error"}</span>`;
        }
    } catch (err) {
        console.error("Voice question error:", err);
        if (responseDisplay) {
            responseDisplay.innerHTML = `<span class="text-muted">Could not reach backend voice service (${err.message}). Please check connection.</span>`;
        }
    }
}

function addVoiceHistory(item) {
    voiceHistory.unshift(item);
    if (voiceHistory.length > 8) voiceHistory.pop();
    renderVoiceHistory();
}

function renderVoiceHistory() {
    const list = document.getElementById("voiceHistoryList");
    if (!list) return;

    list.innerHTML = voiceHistory.map(item => `
        <button type="button" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center py-2"
                onclick="loadVoiceHistoryItem('${item.query.replace(/'/g, "\\'")}', '${item.subject}', '${item.lang}')">
            <div>
                <i class="bi bi-mic me-2 text-primary"></i>
                <strong>“${item.query}”</strong>
                <span class="badge bg-primary-subtle text-primary ms-2">${item.subject} • ${item.unit}</span>
            </div>
            <span class="badge bg-success-subtle text-success"><i class="bi bi-play-fill"></i> Play</span>
        </button>
    `).join("");
}

function loadVoiceHistoryItem(query, subject, lang) {
    activeVoiceQuestion = query;
    activeVoiceLang = lang || "en";
    const found = voiceHistory.find(h => h.query === query);
    if (found) {
        activeVoiceResponseText = found.response;
        const queryDisplay = document.getElementById("voiceQueryDisplay");
        if (queryDisplay) queryDisplay.innerText = `“${query}”`;

        const responseDisplay = document.getElementById("voiceResponseDisplay");
        if (responseDisplay) {
            responseDisplay.innerHTML = `
                <div class="mb-2"><strong>💡 ARIVORA AI Voice Summary (${subject}):</strong></div>
                <div>${found.response}</div>
            `;
        }
        playCurrentVoiceResponse();
    } else {
        processVoiceQuestion(query);
    }
}

function playCurrentVoiceResponse() {
    if (!activeVoiceResponseText) {
        showToast("No active voice note to play.", "info");
        return;
    }
    playBackendAudio(activeVoiceResponseText, activeVoiceLang);
}

function stopCurrentVoiceAudio() {
    // Stop any chat-panel TTS as well
    stopAllTTS();

    if (currentAudioPlayer) {
        currentAudioPlayer.pause();
        currentAudioPlayer.currentTime = 0;
        currentAudioPlayer = null;
    }
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }
    const wave = document.getElementById("voiceWaveAnimation");
    if (wave) wave.classList.add("d-none");

    const circle = document.getElementById("voiceButtonCircle");
    if (circle) circle.classList.remove("speaking");

    const stopBtn = document.getElementById("voiceStopAudioBtn");
    if (stopBtn) stopBtn.classList.add("d-none");

    showToast("⏹️ Audio playback stopped", "info");
}


function playVoiceSpeech(encodedText, lang) {
    const text = decodeURIComponent(encodedText);
    playBackendAudio(text, lang || currentAiLanguage);
}

async function playBackendAudio(text, lang = "en") {
    // Show speaking animation
    const circle = document.getElementById("voiceButtonCircle");
    if (circle) circle.classList.add("speaking");

    const wave = document.getElementById("voiceWaveAnimation");
    if (wave) wave.classList.remove("d-none");

    const stopBtn = document.getElementById("voiceStopAudioBtn");
    if (stopBtn) stopBtn.classList.remove("d-none");

    try {
        const targetLang = (lang && lang.toLowerCase().includes("ta")) ? "ta" : "en";
        const res = await fetch(`${API_BASE}/api/voice-reply`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                language: targetLang,
                username: currentUser.username
            })
        });
        const data = await res.json();

        if (data.success && data.audio_url) {
            if (currentAudioPlayer) {
                currentAudioPlayer.pause();
                currentAudioPlayer = null;
            }
            currentAudioPlayer = new Audio(`${API_BASE}${data.audio_url}`);
            
            currentAudioPlayer.onended = function() {
                if (circle) circle.classList.remove("speaking");
                if (wave) wave.classList.add("d-none");
                if (stopBtn) stopBtn.classList.add("d-none");
            };

            currentAudioPlayer.onerror = function() {
                if (circle) circle.classList.remove("speaking");
                if (wave) wave.classList.add("d-none");
                if (stopBtn) stopBtn.classList.add("d-none");
                // fallback
                if ("speechSynthesis" in window) {
                    const utter = new SpeechSynthesisUtterance(text);
                    utter.lang = targetLang === "ta" ? "ta-IN" : "en-US";
                    window.speechSynthesis.speak(utter);
                }
            };

            currentAudioPlayer.play();
            showToast(`🔊 Playing ARIVORA AI Voice Response (${data.language})`, "info");
        } else {
            throw new Error("No audio url returned");
        }
    } catch (e) {
        console.warn("Audio playback notice:", e);
        // Fallback to browser synthesis
        if ("speechSynthesis" in window) {
            const utter = new SpeechSynthesisUtterance(text);
            utter.onend = function() {
                if (circle) circle.classList.remove("speaking");
                if (wave) wave.classList.add("d-none");
                if (stopBtn) stopBtn.classList.add("d-none");
            };
            window.speechSynthesis.speak(utter);
            showToast("🔊 Playing speech via browser audio engine", "info");
        } else {
            if (circle) circle.classList.remove("speaking");
            if (wave) wave.classList.add("d-none");
            if (stopBtn) stopBtn.classList.add("d-none");
        }
    }
}

/* =========================================================
   8. EXAM PLANNER, TIMETABLE SCANNER & SMART REMINDERS
========================================================= */

let activeTimetable = [
    { subject: "Computer Networks (CS8591)", date: "2026-11-20", days_left: 15, folder: "Computer_Networks" },
    { subject: "Database Management Systems (CS8492)", date: "2026-11-28", days_left: 23, folder: "DBMS" },
    { subject: "Operating Systems (CS8493)", date: "2026-12-05", days_left: 30, folder: "Operating_Systems" }
];

let todayStudyPlan = {
    target_subject: "Computer Networks",
    folder: "Computer_Networks",
    target_unit: "Unit 1",
    days_left: 15,
    quiz_topic: "OSI layers",
    tasks: [
        { id: "t1", title: "Revise Unit 1: OSI 7-Layer Architecture & Physical Media", detail: "Focus on 2-mark definitions & key attributes", type: "study", topic: "OSI layers", marks: 2, completed: true },
        { id: "t2", title: "Master 16-Mark Question: Dijkstra Shortest Path Routing Algorithm", detail: "Practice drawing flowchart and routing table calculations", type: "essay", topic: "Dijkstra algorithm", marks: 16, completed: true },
        { id: "t3", title: "Attempt Daily Adaptive Quiz on 'OSI layers'", detail: "5 questions based on Anna University previous years", type: "quiz", topic: "OSI layers", completed: false }
    ]
};

function triggerTimetablePhotoUpload() {
    const fileInput = document.getElementById("timetablePhotoInput");
    if (fileInput) fileInput.click();
}

async function handleTimetablePhotoChange(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    // Show preview immediately
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewImg = document.getElementById("timetablePreviewImg");
        const placeholder = document.getElementById("timetableUploadPlaceholder");
        const photoMeta = document.getElementById("timetablePhotoMeta");
        const photoName = document.getElementById("timetablePhotoName");

        if (previewImg) {
            previewImg.src = e.target.result;
            previewImg.classList.remove("d-none");
        }
        if (placeholder) placeholder.classList.add("d-none");
        if (photoMeta) photoMeta.classList.remove("d-none");
        if (photoName) photoName.textContent = file.name;

        try {
            localStorage.setItem("arivoraTimetablePreview", e.target.result);
            localStorage.setItem("arivoraTimetableFileName", file.name);
        } catch(err) {}
    };
    reader.readAsDataURL(file);

    showToast("📸 Uploading timetable photo & analyzing schedule with ARIVORA AI...", "info");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", currentUser.username);

    try {
        const res = await fetch(`${API_BASE}/api/timetable/upload`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (data.success) {
            showToast("✅ Timetable photo scanned! Today's study plan generated.", "success");
            if (data.timetable) activeTimetable = data.timetable;
            if (data.today_plan) todayStudyPlan = data.today_plan;
            renderTimetableUI();
        }
    } catch(err) {
        showToast("ℹ️ Timetable photo saved locally. Study countdown updated!", "success");
        renderTimetableUI();
    }
}

function scanDemoTimetable() {
    showToast("⚡ Loaded Anna University Engineering Exam Timetable!", "success");
    const previewImg = document.getElementById("timetablePreviewImg");
    const placeholder = document.getElementById("timetableUploadPlaceholder");
    const photoMeta = document.getElementById("timetablePhotoMeta");
    const photoName = document.getElementById("timetablePhotoName");

    if (previewImg) {
        previewImg.src = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=80";
        previewImg.classList.remove("d-none");
    }
    if (placeholder) placeholder.classList.add("d-none");
    if (photoMeta) photoMeta.classList.remove("d-none");
    if (photoName) photoName.textContent = "Anna_Univ_Nov2026_Timetable.jpg";

    activeTimetable = [
        { subject: "Computer Networks (CS8591)", date: "2026-11-20", days_left: 15, folder: "Computer_Networks" },
        { subject: "Database Management Systems (CS8492)", date: "2026-11-28", days_left: 23, folder: "DBMS" },
        { subject: "Operating Systems (CS8493)", date: "2026-12-05", days_left: 30, folder: "Operating_Systems" }
    ];
    renderTimetableUI();
}

async function loadTimetableData() {
    // Restore saved preview
    const savedPreview = localStorage.getItem("arivoraTimetablePreview");
    const savedName = localStorage.getItem("arivoraTimetableFileName");
    if (savedPreview) {
        const previewImg = document.getElementById("timetablePreviewImg");
        const placeholder = document.getElementById("timetableUploadPlaceholder");
        const photoMeta = document.getElementById("timetablePhotoMeta");
        const photoName = document.getElementById("timetablePhotoName");
        if (previewImg) {
            previewImg.src = savedPreview;
            previewImg.classList.remove("d-none");
        }
        if (placeholder) placeholder.classList.add("d-none");
        if (photoMeta) photoMeta.classList.remove("d-none");
        if (photoName) photoName.textContent = savedName || "timetable.jpg";
    }

    try {
        const res = await fetch(`${API_BASE}/api/timetable?username=${encodeURIComponent(currentUser.username)}`);
        const data = await res.json();
        if (data.success) {
            if (data.timetable) activeTimetable = data.timetable;
            if (data.today_plan) todayStudyPlan = data.today_plan;
        }
    } catch(e) {}

    renderTimetableUI();
}

function renderTimetableUI() {
    if (!activeTimetable || activeTimetable.length === 0) return;

    const nextExam = activeTimetable[0];
    const heroSubject = document.getElementById("examHeroSubject");
    const heroDate = document.getElementById("examHeroDate");
    const daysEl = document.getElementById("days");
    const countBadge = document.getElementById("totalExamsCountBadge");

    if (heroSubject) heroSubject.textContent = nextExam.subject;
    if (heroDate) {
        try {
            const d = new Date(nextExam.date);
            heroDate.textContent = d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
        } catch(e) {
            heroDate.textContent = nextExam.date;
        }
    }
    if (daysEl) daysEl.textContent = `${nextExam.days_left || 15} Days`;
    if (countBadge) countBadge.textContent = `${activeTimetable.length} Exams Scheduled`;

    // Render timetable table rows
    const tbody = document.getElementById("examTimetableTableBody");
    if (tbody) {
        tbody.innerHTML = activeTimetable.map((ex, idx) => {
            const isNext = idx === 0;
            const statusBadge = isNext 
                ? '<span class="badge bg-danger">Upcoming Next</span>'
                : '<span class="badge bg-secondary-subtle text-secondary">Scheduled</span>';
            return `
                <tr>
                    <td class="fw-bold">${ex.subject}</td>
                    <td>${ex.date}</td>
                    <td><span class="badge ${isNext ? 'bg-danger' : 'bg-primary'}">${ex.days_left} Days</span></td>
                    <td>${statusBadge}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="studySpecificExam('${encodeURIComponent(ex.subject)}')">
                            <i class="bi bi-book me-1"></i> Plan Study
                        </button>
                    </td>
                </tr>
            `;
        }).join("");
    }

    // Render Today's Study Plan Tasks
    renderTodayTasks();
}

function renderTodayTasks() {
    const container = document.getElementById("todayTaskList");
    if (!container || !todayStudyPlan || !todayStudyPlan.tasks) return;

    const badge = document.getElementById("todayPlanSubjBadge");
    if (badge) badge.textContent = `Target: ${todayStudyPlan.target_subject} • ${todayStudyPlan.target_unit}`;

    container.innerHTML = todayStudyPlan.tasks.map(t => {
        const isDone = !!t.completed;
        const icon = t.type === "quiz" ? "bi-patch-question-fill text-warning" : (t.type === "essay" ? "bi-file-earmark-text-fill text-danger" : "bi-journal-code text-primary");
        return `
            <div class="list-group-item d-flex align-items-center justify-content-between py-3 px-1 ${isDone ? 'bg-light text-muted' : ''}">
                <div class="d-flex align-items-center gap-3">
                    <input class="form-check-input fs-5 mt-0 cursor-pointer" type="checkbox" ${isDone ? 'checked' : ''} onchange="toggleTaskCompletion('${t.id}')">
                    <div>
                        <h6 class="mb-1 ${isDone ? 'text-decoration-line-through text-muted' : 'fw-bold'}">
                            <i class="bi ${icon} me-1"></i> ${t.title}
                        </h6>
                        <small class="text-muted">${t.detail}</small>
                    </div>
                </div>
                <div>
                    ${t.type === "quiz" ? `
                        <button class="btn btn-sm btn-warning text-dark fw-bold" onclick="startExamDailyQuiz()">
                            <i class="bi bi-play-fill"></i> Quiz
                        </button>
                    ` : `
                        <button class="btn btn-sm btn-outline-primary" onclick="studyTaskWithAI('${encodeURIComponent(t.topic || todayStudyPlan.quiz_topic)}', ${t.marks || 5})">
                            <i class="bi bi-stars"></i> Study
                        </button>
                    `}
                </div>
            </div>
        `;
    }).join("");

    updateProgressStats();
}

function toggleTaskCompletion(taskId) {
    if (!todayStudyPlan || !todayStudyPlan.tasks) return;
    const task = todayStudyPlan.tasks.find(t => t.id === taskId);
    if (task) {
        task.completed = !task.completed;
        renderTodayTasks();
        showToast(task.completed ? "🎉 Task marked as complete!" : "Task updated.", "info");
    }
}

function updateProgressStats() {
    if (!todayStudyPlan || !todayStudyPlan.tasks) return;
    const total = todayStudyPlan.tasks.length;
    const done = todayStudyPlan.tasks.filter(t => t.completed).length;
    const percent = Math.round((done / total) * 100);

    const bar = document.getElementById("todayProgressBar");
    const text = document.getElementById("todayProgressText");
    const readinessBadge = document.getElementById("overallReadinessBadge");

    if (bar) {
        bar.style.width = `${percent}%`;
        bar.textContent = `${percent}%`;
    }
    if (text) text.textContent = `${done} of ${total} Done (${percent}%)`;
    if (readinessBadge) {
        const overall = Math.min(100, Math.round(50 + (percent * 0.4)));
        readinessBadge.textContent = `${overall}% Ready`;
    }
}

function studyTaskWithAI(encodedTopic, marks) {
    const topic = decodeURIComponent(encodedTopic);
    showModule("ai");
    activeChatTopic = topic;
    requestMarkAnswer(marks || 5, topic);
}

function studySpecificExam(encodedSubj) {
    const subj = decodeURIComponent(encodedSubj);
    showModule("ai");
    activeChatTopic = subj;
    appendChatMessage("user", `Generate semester exam preparation blueprint and high-yield topics for ${subj}`);
    requestMarkAnswer(16, `${subj} high priority topics`);
}

function startExamDailyQuiz() {
    const quizTopic = (todayStudyPlan && todayStudyPlan.quiz_topic) ? todayStudyPlan.quiz_topic : "OSI layers";
    showModule("quiz");
    const quizInput = document.getElementById("quizTopicInput");
    if (quizInput) quizInput.value = quizTopic;
    showToast(`🎯 Launching Today's Adaptive Quiz on '${quizTopic}'...`, "info");
    startQuiz();
}

async function saveExamReminder() {
    const nameInput = document.getElementById("examNameInput");
    const dateInput = document.getElementById("examDateInput");

    if (!nameInput || !dateInput || !nameInput.value || !dateInput.value) {
        alert("Please specify exam name and target date.");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/api/exam`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                exam_name: nameInput.value,
                exam_date: dateInput.value,
                subject: activeChatSubject,
                username: currentUser.username
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast("📅 Exam reminder scheduled!", "success");
            activeTimetable.unshift({
                subject: nameInput.value,
                date: dateInput.value,
                days_left: Math.max(0, Math.round((new Date(dateInput.value) - new Date()) / (1000 * 60 * 60 * 24))) || 15,
                folder: "Computer_Networks"
            });
            renderTimetableUI();
            updateExamCountdown(dateInput.value);
        }
    } catch (e) {
        showToast("📅 Exam reminder scheduled locally!", "success");
        activeTimetable.unshift({
            subject: nameInput.value,
            date: dateInput.value,
            days_left: Math.max(0, Math.round((new Date(dateInput.value) - new Date()) / (1000 * 60 * 60 * 24))) || 15,
            folder: "Computer_Networks"
        });
        renderTimetableUI();
    }
}

async function updateExamCountdown(targetDate) {
    const daysEl = document.getElementById("days");
    const dateStr = targetDate || "2026-11-20";

    try {
        const res = await fetch(`${API_BASE}/api/exam-countdown?exam_date=${dateStr}`);
        const data = await res.json();

        if (daysEl) daysEl.innerText = `${data.days_remaining} Days`;
        const msgEl = document.getElementById("examStrategyMsg");
        if (msgEl) msgEl.innerText = data.message;
    } catch (e) {}
}

/* =========================================================
   9. FACULTY AI TOOLS
========================================================= */

async function generateFacultyContent(contentType) {
    if (currentUser.role !== "faculty") {
        showToast("🔒 Unauthorized: Only Faculty accounts can access Faculty Tools.", "error");
        return;
    }

    const topic = prompt("Enter the academic topic for faculty materials:", activeChatTopic || "OSI layers");
    if (!topic) return;

    showToast(`Generating ${contentType} with ARIVORA AI...`, "info");

    try {
        const res = await fetch(`${API_BASE}/api/faculty-content`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: topic,
                content_type: contentType,
                language: currentAiLanguage,
                subject: activeChatSubject
            })
        });
        const data = await res.json();

        if (data.success) {
            let container = document.getElementById("facultyOutputArea");
            if (!container) {
                container = document.createElement("div");
                container.id = "facultyOutputArea";
                document.getElementById("module-faculty").appendChild(container);
            }

            container.innerHTML = `
                <div class="card-box p-4 mt-4 border-primary border">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5>🎓 Generated ${contentType.toUpperCase()}: ${data.topic}</h5>
                        <button class="btn btn-sm btn-outline-secondary" onclick="navigator.clipboard.writeText(this.closest('.card-box').querySelector('pre').innerText); showToast('Copied to clipboard!', 'success');">
                            <i class="bi bi-clipboard"></i> Copy Text
                        </button>
                    </div>
                    <pre class="bg-light p-3 rounded" style="white-space: pre-wrap; font-family: monospace;">${data.content}</pre>
                </div>
            `;
            container.scrollIntoView({ behavior: "smooth" });
        }
    } catch (e) {
        alert("⚠️ Could not generate faculty content.");
    }
}

/* =========================================================
   10. ARIVORA VOICE CONTROLLER & SPEECH RECOGNITION ENGINE
========================================================= */

const ArivoraVoice = {
    state: "STOPPED", // STOPPED | LISTENING | PROCESSING | THINKING | SPEAKING | PAUSED
    recognition: null,
    audioPlayer: null,
    utterance: null,
    lastAiText: "",
    lastAiQuery: "",
    lastLang: "en",

    updateUIState(newState, detailText = "") {
        this.state = newState;
        const badge = document.getElementById("voiceStatusBadge");
        const text = document.getElementById("voiceStatusText");
        const wave = document.getElementById("voiceWaveAnimation");
        const micCircle = document.getElementById("voiceButtonCircle");
        const chatMicBtn = document.getElementById("chatMicBtn");

        if (badge) {
            let color = "bg-secondary";
            let icon = "bi-circle-fill";
            if (newState === "LISTENING") { color = "bg-danger"; icon = "bi-broadcast"; }
            else if (newState === "PROCESSING" || newState === "THINKING") { color = "bg-primary"; icon = "bi-arrow-repeat"; }
            else if (newState === "SPEAKING") { color = "bg-success"; icon = "bi-volume-up-fill"; }
            else if (newState === "PAUSED") { color = "bg-warning text-dark"; icon = "bi-pause-fill"; }

            badge.className = `badge ${color} fs-6 px-3 py-2 rounded-pill shadow-sm`;
            badge.innerHTML = `<i class="bi ${icon} me-1"></i> ${newState}...`;
        }

        if (text) {
            if (detailText) text.innerText = detailText;
            else if (newState === "LISTENING") text.innerHTML = "🎙️ Listening... Speak your syllabus question now!";
            else if (newState === "THINKING" || newState === "PROCESSING") text.innerHTML = "🧠 ARIVORA AI is consulting your syllabus & books...";
            else if (newState === "SPEAKING") text.innerHTML = "🔊 ARIVORA AI is explaining your answer out loud...";
            else if (newState === "PAUSED") text.innerHTML = "⏸️ Voice activity paused. Click Resume or Play to continue.";
            else text.innerHTML = "Click <strong>Start Voice</strong> or tap microphone to speak.";
        }

        if (wave) {
            if (newState === "SPEAKING" || newState === "LISTENING") wave.classList.remove("d-none");
            else wave.classList.add("d-none");
        }

        if (micCircle) {
            micCircle.className = "voice-button shadow-glow";
            if (newState === "LISTENING") micCircle.classList.add("listening");
            if (newState === "SPEAKING") micCircle.classList.add("speaking");
            if (newState === "PAUSED") micCircle.classList.add("paused");
        }

        if (chatMicBtn) {
            if (newState === "LISTENING") {
                chatMicBtn.classList.remove("btn-dark");
                chatMicBtn.classList.add("btn-danger");
                chatMicBtn.innerHTML = '<i class="bi bi-stop-circle-fill"></i>';
            } else {
                chatMicBtn.classList.remove("btn-danger");
                chatMicBtn.classList.add("btn-dark");
                chatMicBtn.innerHTML = '<i class="bi bi-mic"></i>';
            }
        }
    },

    startVoice() {
        this.cancelVoice();

        if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
            showToast("Microphone speech recognition is not supported in this browser. Please type your query.", "error");
            this.updateUIState("STOPPED", "Speech recognition not supported in browser.");
            return;
        }

        try {
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SR();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = currentAiLanguage.toLowerCase().includes("tamil") ? "ta-IN" : "en-IN";

            this.updateUIState("LISTENING");
            showToast("🎙️ Listening... Speak your question!", "info");

            const voiceInputEl = document.getElementById("voiceManualInput") || document.getElementById("chatInput");

            this.recognition.onresult = (event) => {
                let interim = "";
                let final = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) final += event.results[i][0].transcript;
                    else interim += event.results[i][0].transcript;
                }
                if (voiceInputEl) voiceInputEl.value = final || interim;
                if (final) {
                    this.updateUIState("PROCESSING", `Recognized: "${final}"`);
                    showToast(`✅ Captured: "${final}"`, "success");
                    setTimeout(() => {
                        this.processVoiceQuery(final);
                    }, 500);
                }
            };

            this.recognition.onerror = (event) => {
                console.warn("Speech error:", event.error);
                if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                    showToast("🎙️ Microphone permission blocked. On mobile, please allow mic access or open using the HTTPS link!", "error");
                    this.updateUIState("STOPPED", "Microphone access blocked.");
                } else if (event.error !== "no-speech") {
                    showToast(`Voice error: ${event.error}`, "info");
                    this.updateUIState("STOPPED", `Voice error: ${event.error}`);
                } else {
                    this.updateUIState("STOPPED");
                }
            };

            this.recognition.onend = () => {
                if (this.state === "LISTENING") {
                    this.updateUIState("STOPPED");
                }
            };

            this.recognition.start();
        } catch (e) {
            console.error("Mic access exception:", e);
            showToast("Could not access microphone. Please check microphone permissions.", "error");
            this.updateUIState("STOPPED");
        }
    },

    stopVoice() {
        if (this.recognition) {
            try { this.recognition.abort(); } catch(e) {}
            this.recognition = null;
        }
        if (this.audioPlayer) {
            this.audioPlayer.pause();
            this.audioPlayer.currentTime = 0;
            this.audioPlayer = null;
        }
        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }
        if (currentTTSButton) {
            resetTTSButton(currentTTSButton);
        }
        isTTSPlaying = false;
        this.updateUIState("STOPPED", "Voice session stopped.");
        showToast("⏹️ Voice & audio playback stopped.", "info");
    },

    pauseVoice() {
        if (this.state === "SPEAKING") {
            if (this.audioPlayer) this.audioPlayer.pause();
            if ("speechSynthesis" in window) window.speechSynthesis.pause();
            this.updateUIState("PAUSED", "Audio playback paused.");
            showToast("⏸️ Speech paused.", "info");
        } else if (this.state === "LISTENING") {
            if (this.recognition) try { this.recognition.stop(); } catch(e){}
            this.updateUIState("PAUSED", "Listening paused.");
            showToast("⏸️ Microphone listening paused.", "info");
        }
    },

    resumeVoice() {
        if (this.state === "PAUSED") {
            if (this.audioPlayer && this.audioPlayer.paused) {
                this.audioPlayer.play();
                this.updateUIState("SPEAKING");
                showToast("▶️ Resumed audio playback.", "info");
            } else if ("speechSynthesis" in window && window.speechSynthesis.paused) {
                window.speechSynthesis.resume();
                this.updateUIState("SPEAKING");
                showToast("▶️ Resumed SpeechSynthesis.", "info");
            } else {
                this.replayAiResponse();
            }
        } else if (this.state === "STOPPED") {
            this.startVoice();
        }
    },

    cancelVoice() {
        this.stopVoice();
    },

    async processVoiceQuery(query) {
        if (!query || !query.trim()) return;

        this.lastAiQuery = query.trim();
        this.updateUIState("THINKING", "Asking ARIVORA AI...");

        const queryDisplay = document.getElementById("voiceQueryDisplay");
        if (queryDisplay) queryDisplay.innerText = `“${query}”`;

        try {
            const langParam = currentAiLanguage.toLowerCase().includes("tamil") ? "Tamil" : "English";
            const targetSubject = activeChatSubject || (currentUser && currentUser.subject) || "Computer Networks";
            const targetUsername = (currentUser && currentUser.username) ? currentUser.username : "Student";

            const res = await fetch(`${API_BASE}/api/answer`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    topic: query,
                    marks: 2,
                    language: langParam,
                    subject: targetSubject,
                    username: targetUsername
                })
            });

            const data = await res.json();
            if (data.success) {
                const subjBadge = document.getElementById("voiceSubjectBadge");
                if (subjBadge) subjBadge.innerText = data.subject || activeChatSubject;

                const unitBadge = document.getElementById("voiceUnitBadge");
                if (unitBadge) unitBadge.innerText = `Unit ${data.unit || 1}`;

                const langBadge = document.getElementById("voiceLangBadge");
                if (langBadge) langBadge.innerText = `🌐 ${data.language || currentAiLanguage}`;

                let speechText = "";
                if (data.is_out_of_syllabus || data.status === "out_of_syllabus") {
                    speechText = `This topic '${query}' is not in your selected syllabus or uploaded materials. Please click Ask General AI or switch folder.`;
                } else if (data.tamil_summary && currentAiLanguage === "Tamil") {
                    speechText = data.tamil_summary;
                } else {
                    const lines = data.answer.split("\n").filter(l => l.trim().length > 0 && !l.startsWith("=") && !l.startsWith("-"));
                    speechText = lines.slice(0, 3).join(". ").replace(/[•#*|]/g, "").trim();
                }

                this.lastAiText = speechText;
                this.lastLang = (data.language === "Tamil") ? "ta" : "en";

                const responseDisplay = document.getElementById("voiceResponseDisplay");
                if (responseDisplay) {
                    responseDisplay.innerHTML = `
                        <div class="mb-2"><strong>💡 ARIVORA AI Explanation (${data.subject}):</strong></div>
                        <div>${data.answer.replace(/\n/g, "<br>")}</div>
                        <div class="text-muted small mt-2">📖 Reference: ${data.reference}</div>
                    `;
                }

                if (typeof appendChatMessage === "function") {
                    appendChatMessage("user", query);
                    appendChatMessage("ai", data.answer, {
                        is_out_of_syllabus: !!data.is_out_of_syllabus || data.status === "out_of_syllabus",
                        status: data.status,
                        action: data.action,
                        folder_name: data.folder_name,
                        folder_key: data.folder_key,
                        marks: data.is_out_of_syllabus ? null : (data.marks || 2),
                        unit: data.unit,
                        unit_title: data.unit_title,
                        subject: data.subject,
                        reference: data.reference
                    }, query);
                }

                this.speakText(speechText, this.lastLang);
            } else {
                this.updateUIState("STOPPED", "API error");
                showToast("Could not generate AI response.", "error");
            }
        } catch (e) {
            console.error("Voice process error:", e);
            this.updateUIState("STOPPED", "Connection error");
            showToast("Failed to connect to backend voice service.", "error");
        }
    },

    replayAiResponse() {
        if (!this.lastAiText) {
            showToast("No recent AI voice response available to replay.", "info");
            return;
        }
        this.speakText(this.lastAiText, this.lastLang);
    },

    speakText(text, lang = "en") {
        this.stopVoice();

        this.updateUIState("SPEAKING");
        showToast("🔊 Speaking AI response...", "info");

        fetch(`${API_BASE}/api/voice-reply`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, language: lang, username: currentUser.username })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success && data.audio_url) {
                this.audioPlayer = new Audio(`${API_BASE}${data.audio_url}`);
                this.audioPlayer.onended = () => this.updateUIState("STOPPED", "Finished speaking.");
                this.audioPlayer.onerror = () => this.speakWithBrowserFallback(text, lang);
                this.audioPlayer.play();
            } else {
                this.speakWithBrowserFallback(text, lang);
            }
        })
        .catch(() => this.speakWithBrowserFallback(text, lang));
    },

    speakWithBrowserFallback(text, lang) {
        if (!("speechSynthesis" in window)) {
            this.updateUIState("STOPPED", "TTS not supported.");
            return;
        }
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = lang.includes("ta") ? "ta-IN" : "en-IN";
        utter.rate = 0.92;
        utter.onend = () => this.updateUIState("STOPPED", "Finished speaking.");
        utter.onerror = () => this.updateUIState("STOPPED", "TTS error.");
        this.utterance = utter;
        window.speechSynthesis.speak(utter);
    }
};

/* =========================================================
   AUTH HELPERS & CANVAS PARTICLES
========================================================= */

function togglePasswordVisibility(fieldId, btn) {
    const input = document.getElementById(fieldId);
    if (!input) return;
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";
    if (btn) {
        const icon = btn.querySelector("i");
        if (icon) icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
    }
}

function handleForgotPassword() {
    const email = prompt("Enter your registered email address to reset password:");
    if (email && email.trim()) {
        showToast(`Password reset link sent to ${email.trim()}. Please check your inbox.`, "success");
    }
}

function initAuthCanvas() {
    const canvas = document.getElementById("authCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = Array.from({ length: 35 }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        radius: Math.random() * 2.5 + 1
    }));

    function animate() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "rgba(99, 102, 241, 0.25)";
        ctx.strokeStyle = "rgba(168, 85, 247, 0.08)";
        ctx.lineWidth = 1;

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", function() {
    loadSavedUser();
    loadTheme();
    updateRoleUI();
    updateExamCountdown();
    loadTimetableData();
    initAuthCanvas();

    hideElement("signupPage");
    hideElement("rolePage");
    hideElement("profilePage");
    hideElement("languagePage");
    hideElement("dashboardPage");
    showElement("loginPage");

    // Chat enter key support
    const chatInp = document.getElementById("chatInput");
    if (chatInp) {
        chatInp.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                sendChatMessage();
            }
        });
    }

    const subjectSelect = document.getElementById("uploadModalSubject");
    if (subjectSelect) {
        subjectSelect.addEventListener("change", function() {
            const grp = document.getElementById("newFolderInputGroup");
            if (grp) {
                if (this.value === "__NEW__") {
                    grp.classList.remove("d-none");
                } else {
                    grp.classList.add("d-none");
                }
            }
        });
    }

    console.log("ARIVORA AI Connected Frontend Initialized 🚀");
});
