# ================================================================
# 🚀 CAREERPILOT-X 2.0
# Secure AI Career Intelligence Platform
#
# FULL FEATURES:
# 🔐 Login / Signup / Logout
# 🛡️ Security & Privacy Center
# 👤 Student Profile
# 🏠 Career Intelligence Dashboard
# 🔎 Job / Internship Search
# ✅ Original Source Verification
# 🚨 Fake Job Detection
# 🎯 Skill Matching
# 📝 Resume Analyzer
# 🚀 Career Mission
# 🧬 Career Digital Twin
# 🔬 What-If Career Lab
# 🧬 Opportunity DNA
# 🎤 Interview Simulator
# 📋 Application Tracking
#
# RENDER READY
# No /content path
# ================================================================

import os
import re
import sqlite3
import hashlib
import secrets
import tempfile
import random
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

# Optional packages
try:
    import bcrypt
except ImportError:
    bcrypt = None

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


# ================================================================
# PAGE CONFIG
# ================================================================

st.set_page_config(
    page_title="CareerPilot-X 2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
# RENDER-SAFE STORAGE
# ================================================================
#
# NEVER USE:
# /content
#
# /content is a Google Colab path and caused your Render error.
#
# SQLite database is stored in the application directory when
# possible. Render's local filesystem is ephemeral, so for a
# production multi-instance application you should eventually use
# PostgreSQL or another persistent database.
# ================================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "careerpilot_data"

try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    DATA_DIR = Path(tempfile.gettempdir()) / "careerpilot_data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "careerpilot.db"


# ================================================================
# DATABASE
# ================================================================

def get_db():
    conn = sqlite3.connect(
        str(DB_PATH),
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            education TEXT,
            target_career TEXT,
            skills TEXT,
            projects TEXT,
            certifications TEXT,
            experience TEXT,
            phone TEXT,
            location TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT,
            role TEXT,
            url TEXT,
            status TEXT,
            risk_score INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ================================================================
# PASSWORD SECURITY
# ================================================================

def hash_password(password):

    if bcrypt:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    # Fallback if bcrypt is unavailable
    salt = secrets.token_hex(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        120000
    ).hex()

    return f"PBKDF2${salt}${digest}"


def verify_password(password, stored_hash):

    if stored_hash.startswith("PBKDF2$"):

        try:
            _, salt, expected = stored_hash.split("$")

            actual = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt.encode(),
                120000
            ).hex()

            return secrets.compare_digest(
                actual,
                expected
            )

        except Exception:
            return False

    if bcrypt:

        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )
        except Exception:
            return False

    return False


# ================================================================
# SESSION STATE
# ================================================================

DEFAULT_STATE = {
    "authenticated": False,
    "user_id": None,
    "username": None,
    "email": None,
    "interview_question": None,
    "interview_score": None
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ================================================================
# AUTH FUNCTIONS
# ================================================================

def create_user(username, email, password):

    conn = get_db()

    try:

        conn.execute(
            """
            INSERT INTO users
            (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                username.strip(),
                email.strip().lower(),
                hash_password(password)
            )
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Username or email already exists."

    finally:
        conn.close()


def authenticate_user(identifier, password):

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        OR email = ?
        """,
        (
            identifier.strip(),
            identifier.strip().lower()
        )
    ).fetchone()

    conn.close()

    if not user:
        return None

    if verify_password(
        password,
        user["password_hash"]
    ):

        return user

    return None


def logout():

    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.email = None

    st.rerun()


# ================================================================
# PROFILE FUNCTIONS
# ================================================================

def get_profile(user_id):

    conn = get_db()

    profile = conn.execute(
        """
        SELECT *
        FROM profiles
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    return profile


def save_profile(
    user_id,
    name,
    education,
    target_career,
    skills,
    projects,
    certifications,
    experience,
    phone,
    location
):

    conn = get_db()

    conn.execute(
        """
        INSERT INTO profiles
        (
            user_id,
            name,
            education,
            target_career,
            skills,
            projects,
            certifications,
            experience,
            phone,
            location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            name=excluded.name,
            education=excluded.education,
            target_career=excluded.target_career,
            skills=excluded.skills,
            projects=excluded.projects,
            certifications=excluded.certifications,
            experience=excluded.experience,
            phone=excluded.phone,
            location=excluded.location,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            user_id,
            name,
            education,
            target_career,
            skills,
            projects,
            certifications,
            experience,
            phone,
            location
        )
    )

    conn.commit()
    conn.close()


# ================================================================
# CAREER DATABASE
# ================================================================

CAREERS = {

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Statistics",
        "NumPy",
        "Pandas",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch"
    ],

    "Generative AI Engineer": [
        "Python",
        "Generative AI",
        "LLMs",
        "Prompt Engineering",
        "RAG",
        "NLP",
        "Vector Databases"
    ],

    "Data Scientist": [
        "Python",
        "Statistics",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "SQL",
        "Data Visualization"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Power BI",
        "Data Visualization"
    ],

    "Software Developer": [
        "Python",
        "Java",
        "Data Structures",
        "Algorithms",
        "OOP",
        "Git",
        "SQL"
    ],

    "Cybersecurity Analyst": [
        "Python",
        "Linux",
        "Networking",
        "Cybersecurity",
        "Ethical Hacking",
        "Security Tools"
    ],

    "Cloud Engineer": [
        "Linux",
        "Networking",
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes"
    ],

    "DevOps Engineer": [
        "Linux",
        "Git",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "AWS"
    ],

    "NLP Engineer": [
        "Python",
        "NLP",
        "Machine Learning",
        "Deep Learning",
        "Transformers",
        "LLMs"
    ],

    "AI Product Manager": [
        "AI Fundamentals",
        "Product Management",
        "Analytics",
        "Communication",
        "User Research",
        "Business Strategy"
    ]
}


# ================================================================
# INTERVIEW DATABASE
# ================================================================

INTERVIEW_QUESTIONS = {

    "AI/ML Engineer": [
        "What is Machine Learning?",
        "What is Generative AI?",
        "What is NLP?",
        "How would you deploy a Machine Learning model?",
        "What is feature engineering?",
        "What is overfitting and how can you prevent it?",
        "What is the difference between supervised and unsupervised learning?",
        "What is cross-validation?",
        "What is model evaluation?",
        "How would you improve a machine learning model?"
    ],

    "Generative AI Engineer": [
        "What is Generative AI?",
        "What is an LLM?",
        "What is prompt engineering?",
        "What is RAG?",
        "What is a vector database?",
        "What is hallucination?",
        "How can RAG reduce hallucinations?",
        "What are embeddings?"
    ],

    "Data Scientist": [
        "What is data preprocessing?",
        "What is feature engineering?",
        "What is regression?",
        "What is classification?",
        "What is overfitting?",
        "What is cross-validation?",
        "What is exploratory data analysis?"
    ],

    "Data Analyst": [
        "What is data analysis?",
        "What is SQL?",
        "What is an SQL JOIN?",
        "What is data visualization?",
        "What is the difference between mean and median?"
    ],

    "Software Developer": [
        "What is Object-Oriented Programming?",
        "What is inheritance?",
        "What is polymorphism?",
        "What is a data structure?",
        "What is an algorithm?",
        "What is Git?",
        "What is the difference between Python and Java?"
    ],

    "Cybersecurity Analyst": [
        "What is cybersecurity?",
        "What is phishing?",
        "What is malware?",
        "What is encryption?",
        "What is authentication?",
        "What is a firewall?"
    ],

    "Cloud Engineer": [
        "What is cloud computing?",
        "What is AWS?",
        "What is virtualization?",
        "What is Docker?",
        "What is Kubernetes?"
    ],

    "DevOps Engineer": [
        "What is DevOps?",
        "What is CI/CD?",
        "What is Docker?",
        "What is Kubernetes?",
        "What is Git?"
    ],

    "NLP Engineer": [
        "What is NLP?",
        "What is tokenization?",
        "What are embeddings?",
        "What is a Transformer?",
        "What is an LLM?"
    ],

    "AI Product Manager": [
        "What is an AI product?",
        "How do you define product requirements?",
        "How would you evaluate an AI product?",
        "What is user research?",
        "What is product-market fit?"
    ]
}


# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def normalize(text):

    return re.sub(
        r"[^a-z0-9+#]",
        "",
        str(text).lower()
    )


def split_skills(text):

    if not text:
        return []

    return [
        item.strip()
        for item in re.split(
            r"[,;\n]",
            text
        )
        if item.strip()
    ]


def skill_match(user_skills, required_skills):

    user = {
        normalize(x)
        for x in user_skills
    }

    required = {
        normalize(x)
        for x in required_skills
    }

    if not required:
        return 0

    return round(
        len(user & required)
        / len(required)
        * 100
    )


def missing_skills(user_skills, required):

    user = {
        normalize(x)
        for x in user_skills
    }

    return [
        skill
        for skill in required
        if normalize(skill) not in user
    ]


# ================================================================
# URL SECURITY ANALYSIS
# ================================================================

SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "cutt.ly",
    "rb.gy"
}

SUSPICIOUS_TLDS = {
    ".click",
    ".top",
    ".xyz",
    ".buzz",
    ".monster",
    ".work"
}


def analyze_url(url):

    findings = []
    score = 0

    url = url.strip()

    if not url:
        return 0, findings

    if not re.match(
        r"^https?://",
        url,
        re.I
    ):
        url = "https://" + url

    try:

        parsed = urlparse(url)
        host = parsed.hostname or ""

        host = host.lower()

        if parsed.scheme != "https":
            findings.append(
                "⚠️ URL does not use HTTPS."
            )
            score += 15

        if host in SHORTENERS:
            findings.append(
                "⚠️ URL uses a known URL-shortening service."
            )
            score += 20

        if re.match(
            r"^\d+\.\d+\.\d+\.\d+$",
            host
        ):
            findings.append(
                "🚨 URL uses an IP address instead of a domain."
            )
            score += 30

        if any(
            host.endswith(tld)
            for tld in SUSPICIOUS_TLDS
        ):
            findings.append(
                "⚠️ Domain uses a higher-risk TLD."
            )
            score += 15

        if "@" in url:
            findings.append(
                "🚨 URL contains an @ symbol."
            )
            score += 25

        if len(url) > 150:
            findings.append(
                "⚠️ URL is unusually long."
            )
            score += 10

        suspicious_words = [
            "login",
            "verify",
            "urgent",
            "payment",
            "fee",
            "reward",
            "claim",
            "account"
        ]

        found_words = [
            word
            for word in suspicious_words
            if word in url.lower()
        ]

        if found_words:

            findings.append(
                "⚠️ URL contains sensitive/action words: "
                + ", ".join(found_words)
            )

            score += min(
                len(found_words) * 5,
                20
            )

        return min(score, 100), findings

    except Exception:

        return 50, [
            "⚠️ URL could not be parsed safely."
        ]


# ================================================================
# JOB SCAM ANALYSIS
# ================================================================

SCAM_PATTERNS = {

    "payment": [
        "registration fee",
        "registration fees",
        "pay fee",
        "pay a fee",
        "training fee",
        "security deposit",
        "processing fee",
        "joining fee",
        "refundable fee",
        "pay money",
        "send money"
    ],

    "personal_data": [
        "otp",
        "one time password",
        "cvv",
        "credit card",
        "debit card",
        "bank password",
        "upi pin",
        "atm pin"
    ],

    "urgency": [
        "act immediately",
        "limited slots",
        "urgent hiring",
        "apply immediately",
        "today only",
        "within 24 hours"
    ],

    "unrealistic": [
        "earn ₹1 lakh",
        "earn rs 100000",
        "guaranteed income",
        "guaranteed job",
        "no skills required",
        "earn millions",
        "make money instantly"
    ],

    "suspicious": [
        "whatsapp only",
        "telegram only",
        "contact me privately",
        "send documents immediately",
        "pay before interview"
    ]
}


def analyze_job(
    company,
    role,
    description,
    salary,
    url
):

    text = " ".join([
        company or "",
        role or "",
        description or "",
        salary or "",
        url or ""
    ]).lower()

    score = 0
    reasons = []

    for category, patterns in SCAM_PATTERNS.items():

        for pattern in patterns:

            if pattern in text:

                if category == "payment":
                    score += 35
                    reasons.append(
                        "🚨 Payment/fee request detected."
                    )

                elif category == "personal_data":
                    score += 35
                    reasons.append(
                        "🚨 Request for highly sensitive information detected."
                    )

                elif category == "urgency":
                    score += 15
                    reasons.append(
                        "⚠️ High-pressure/urgency language detected."
                    )

                elif category == "unrealistic":
                    score += 20
                    reasons.append(
                        "⚠️ Potentially unrealistic job claim detected."
                    )

                elif category == "suspicious":
                    score += 15
                    reasons.append(
                        "⚠️ Suspicious communication/application pattern detected."
                    )

                break

    url_score, url_findings = analyze_url(url)

    score += int(url_score * 0.5)

    reasons.extend(url_findings)

    # Salary heuristic
    salary_numbers = re.findall(
        r"\d+(?:,\d+)*(?:\.\d+)?",
        salary or ""
    )

    if salary_numbers:

        try:

            values = [
                float(x.replace(",", ""))
                for x in salary_numbers
            ]

            maximum = max(values)

            if maximum > 200000:
                score += 15
                reasons.append(
                    "⚠️ Compensation appears unusually high and should be verified."
                )

        except Exception:
            pass

    score = min(score, 100)

    if score >= 70:
        level = "🔴 HIGH RISK / POTENTIAL FAKE"

    elif score >= 35:
        level = "🟡 NEEDS VERIFICATION"

    else:
        level = "🟢 LOWER RISK"

    return score, level, list(dict.fromkeys(reasons))


# ================================================================
# SOURCE VERIFICATION
# ================================================================

def domain_matches_company(url, company):

    if not url or not company:
        return False

    try:

        host = urlparse(
            url if url.startswith("http")
            else "https://" + url
        ).hostname or ""

        company_words = re.findall(
            r"[a-zA-Z0-9]+",
            company.lower()
        )

        host_clean = re.sub(
            r"[^a-z0-9]",
            "",
            host.lower()
        )

        return any(
            normalize(word) in host_clean
            for word in company_words
            if len(normalize(word)) >= 4
        )

    except Exception:

        return False


def verify_job_source(company, url, description):

    score = 50
    reasons = []

    if not url:

        return 20, "🟡 SOURCE NOT PROVIDED", [
            "No application URL was provided."
        ]

    url_score, url_findings = analyze_url(url)

    score -= int(url_score * 0.5)

    reasons.extend(url_findings)

    if domain_matches_company(
        url,
        company
    ):

        score += 30

        reasons.append(
            "✅ Application domain appears related to the company name."
        )

    else:

        reasons.append(
            "⚠️ Application domain could not be confidently matched to the company."
        )

    if requests:

        try:

            response = requests.get(
                url,
                timeout=7,
                headers={
                    "User-Agent":
                    "CareerPilot-X/2.0"
                },
                allow_redirects=True
            )

            if response.status_code < 400:

                score += 15

                reasons.append(
                    "✅ Application page responded successfully."
                )

            else:

                score -= 15

                reasons.append(
                    f"⚠️ Application page returned HTTP {response.status_code}."
                )

        except Exception:

            reasons.append(
                "⚠️ The application page could not be reached automatically."
            )

    score = max(
        0,
        min(score, 100)
    )

    if score >= 80:
        label = "🟢 LIKELY ORIGINAL / LOWER RISK"

    elif score >= 50:
        label = "🟡 VERIFY BEFORE APPLYING"

    else:
        label = "🔴 SOURCE COULD NOT BE VERIFIED"

    return score, label, list(dict.fromkeys(reasons))


# ================================================================
# RESUME ANALYSIS
# ================================================================

def extract_resume_text(uploaded_file):

    if uploaded_file is None:
        return ""

    try:

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".txt"):

            return uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            )

        if file_name.endswith(".pdf"):

            try:

                import PyPDF2

                reader = PyPDF2.PdfReader(
                    uploaded_file
                )

                return "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

            except Exception:

                return ""

        return ""

    except Exception:

        return ""


def analyze_resume(text):

    detected = []

    all_skills = set()

    for skills in CAREERS.values():
        all_skills.update(skills)

    lower = text.lower()

    for skill in all_skills:

        if skill.lower() in lower:
            detected.append(skill)

    return sorted(detected)


# ================================================================
# INTERVIEW EVALUATION
# ================================================================

def evaluate_answer(answer):

    if not answer.strip():

        return 0, [
            "No answer was provided."
        ]

    words = answer.lower().split()

    technical_terms = [
        "model",
        "data",
        "algorithm",
        "training",
        "testing",
        "feature",
        "prediction",
        "accuracy",
        "python",
        "machine",
        "learning",
        "ai",
        "generative",
        "llm",
        "rag",
        "nlp",
        "deployment",
        "overfitting",
        "example"
    ]

    matched = sum(
        term in words
        for term in technical_terms
    )

    length_score = min(
        len(words) / 50,
        1
    )

    score = int(
        min(
            100,
            matched * 7 +
            length_score * 40
        )
    )

    feedback = []

    if score >= 75:
        feedback.append(
            "Excellent technical response."
        )

    elif score >= 50:
        feedback.append(
            "Good response, but add more technical depth."
        )

    else:
        feedback.append(
            "Try explaining the concept with a definition and example."
        )

    if len(words) < 15:

        feedback.append(
            "Your answer is quite short."
        )

    else:

        feedback.append(
            "Good answer length."
        )

    return score, feedback


# ================================================================
# APPLICATION DATABASE
# ================================================================

def save_application(
    user_id,
    company,
    role,
    url,
    status,
    risk_score,
    notes
):

    conn = get_db()

    conn.execute(
        """
        INSERT INTO applications
        (
            user_id,
            company,
            role,
            url,
            status,
            risk_score,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            company,
            role,
            url,
            status,
            risk_score,
            notes
        )
    )

    conn.commit()
    conn.close()


def get_applications(user_id):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return rows


def delete_application(app_id, user_id):

    conn = get_db()

    conn.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        AND user_id = ?
        """,
        (
            app_id,
            user_id
        )
    )

    conn.commit()
    conn.close()


# ================================================================
# CSS
# ================================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .security-card {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ================================================================
# LOGIN PAGE
# ================================================================

def login_page():

    st.markdown(
        '<div class="main-title">🚀 CareerPilot-X 2.0</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Secure AI Career Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        [
            "🔐 Login",
            "🆕 Create Account"
        ]
    )

    with login_tab:

        st.subheader("Welcome Back")

        identifier = st.text_input(
            "Username or Email",
            key="login_identifier"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if not identifier or not password:

                st.warning(
                    "Enter your username/email and password."
                )

            else:

                user = authenticate_user(
                    identifier,
                    password
                )

                if user:

                    st.session_state.authenticated = True
                    st.session_state.user_id = user["id"]
                    st.session_state.username = user["username"]
                    st.session_state.email = user["email"]

                    st.success(
                        "Login successful."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username/email or password."
                    )

    with signup_tab:

        st.subheader("Create Your CareerPilot Account")

        new_username = st.text_input(
            "Username",
            key="signup_username"
        )

        new_email = st.text_input(
            "Email",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm"
        )

        if st.button(
            "🆕 Create Account",
            use_container_width=True
        ):

            if not new_username or not new_email or not new_password:

                st.warning(
                    "Please complete all required fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 8:

                st.error(
                    "Password should contain at least 8 characters."
                )

            elif "@" not in new_email:

                st.error(
                    "Enter a valid email address."
                )

            else:

                success, message = create_user(
                    new_username,
                    new_email,
                    new_password
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)

    st.markdown("---")

    st.info(
        "🔒 Your password is stored as a cryptographic hash. "
        "Never enter OTPs, UPI PINs, card PINs or banking passwords "
        "into CareerPilot-X."
    )


# ================================================================
# SHOW LOGIN IF NOT AUTHENTICATED
# ================================================================

if not st.session_state.authenticated:

    login_page()
    st.stop()


# ================================================================
# APP HEADER
# ================================================================

st.markdown(
    '<div class="main-title">🚀 CareerPilot-X 2.0</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Find opportunities. Verify them. Protect yourself. Build your career.'
    '</div>',
    unsafe_allow_html=True
)


# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("🧭 CareerPilot-X")

st.sidebar.success(
    f"👤 {st.session_state.username}"
)

pages = [
    "🏠 Career Intelligence",
    "👤 Student Profile",
    "🔎 Verified Job Search",
    "🚨 Fake Job Detector",
    "🧬 Opportunity DNA",
    "🎯 Skill Matching",
    "📝 Resume Analyzer",
    "🚀 Career Mission",
    "🧬 Career Digital Twin",
    "🔬 What-If Career Lab",
    "🎤 Interview Simulator",
    "📋 Application Tracking",
    "🛡️ Security & Privacy"
]

page = st.sidebar.radio(
    "Navigate",
    pages
)

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    logout()


# ================================================================
# GET PROFILE
# ================================================================

profile = get_profile(
    st.session_state.user_id
)


# ================================================================
# 1. CAREER INTELLIGENCE DASHBOARD
# ================================================================

if page == "🏠 Career Intelligence":

    st.header("🏠 Career Intelligence Dashboard")

    user_skills = []

    if profile and profile["skills"]:
        user_skills = split_skills(
            profile["skills"]
        )

    target = (
        profile["target_career"]
        if profile and profile["target_career"]
        else "AI/ML Engineer"
    )

    required = CAREERS.get(
        target,
        CAREERS["AI/ML Engineer"]
    )

    match = skill_match(
        user_skills,
        required
    )

    applications = get_applications(
        st.session_state.user_id
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🎯 Skill Match",
            f"{match}%"
        )

    with col2:
        st.metric(
            "📋 Applications",
            len(applications)
        )

    with col3:
        st.metric(
            "🧠 Target Career",
            target
        )

    with col4:
        st.metric(
            "🔐 Security",
            "ACTIVE"
        )

    st.markdown("---")

    st.subheader(
        "🎯 Your Career Direction"
    )

    st.info(
        f"Your selected target career is **{target}**."
    )

    missing = missing_skills(
        user_skills,
        required
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Your Skills")

        if user_skills:

            for skill in user_skills:
                st.write(
                    f"• {skill}"
                )

        else:

            st.warning(
                "Complete your Student Profile."
            )

    with col2:

        st.subheader("📚 Skills to Develop")

        if missing:

            for skill in missing[:8]:
                st.write(
                    f"• {skill}"
                )

        else:

            st.success(
                "Your listed skills cover the current career requirements."
            )

    st.markdown("---")

    st.subheader(
        "🛡️ Career Safety"
    )

    st.write(
        "CareerPilot-X evaluates job opportunities for suspicious "
        "signals before you apply. Always verify important information "
        "through the employer's official channels."
    )


# ================================================================
# 2. STUDENT PROFILE
# ================================================================

elif page == "👤 Student Profile":

    st.header("👤 Student Profile")

    st.info(
        "Your profile is associated with your account and is not "
        "displayed to other users by this application."
    )

    current = profile

    name = st.text_input(
        "Full Name",
        value=current["name"] if current else ""
    )

    education = st.text_input(
        "Education",
        value=current["education"]
        if current else ""
    )

    target_career = st.selectbox(
        "Target Career",
        list(CAREERS.keys()),
        index=(
            list(CAREERS.keys()).index(
                current["target_career"]
            )
            if current
            and current["target_career"]
            in CAREERS
            else 0
        )
    )

    skills = st.text_area(
        "Skills",
        value=current["skills"]
        if current else
        "Python, Java, Machine Learning"
    )

    projects = st.text_area(
        "Projects",
        value=current["projects"]
        if current else ""
    )

    certifications = st.text_area(
        "Certifications",
        value=current["certifications"]
        if current else ""
    )

    experience = st.text_area(
        "Experience / Internship",
        value=current["experience"]
        if current else ""
    )

    col1, col2 = st.columns(2)

    with col1:

        phone = st.text_input(
            "Phone",
            value=current["phone"]
            if current else ""
        )

    with col2:

        location = st.text_input(
            "Location",
            value=current["location"]
            if current else ""
        )

    st.warning(
        "Do not enter passwords, OTPs, UPI PINs, bank credentials, "
        "card PINs or other secrets into your profile."
    )

    if st.button(
        "💾 Save Profile",
        use_container_width=True
    ):

        save_profile(
            st.session_state.user_id,
            name,
            education,
            target_career,
            skills,
            projects,
            certifications,
            experience,
            phone,
            location
        )

        st.success(
            "Profile saved securely."
        )

        st.rerun()


# ================================================================
# 3. VERIFIED JOB SEARCH
# ================================================================

elif page == "🔎 Verified Job Search":

    st.header("🔎 Verified Job Search")

    st.write(
        "Enter a job/internship opportunity you found. "
        "CareerPilot-X checks the URL, company relationship, "
        "job text and scam indicators."
    )

    company = st.text_input(
        "Company Name"
    )

    role = st.text_input(
        "Job / Internship Role"
    )

    salary = st.text_input(
        "Salary / Stipend"
    )

    url = st.text_input(
        "Application URL"
    )

    description = st.text_area(
        "Job Description",
        height=220
    )

    if st.button(
        "🛡️ Verify Opportunity",
        use_container_width=True
    ):

        if not company or not role:

            st.warning(
                "Enter at least the company and role."
            )

        else:

            risk_score, risk_level, risk_reasons = analyze_job(
                company,
                role,
                description,
                salary,
                url
            )

            source_score, source_label, source_reasons = verify_job_source(
                company,
                url,
                description
            )

            overall_score = int(
                risk_score * 0.6 +
                (100 - source_score) * 0.4
            )

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🚨 Risk Score",
                    f"{risk_score}/100"
                )

            with col2:
                st.metric(
                    "🔗 Source Confidence",
                    f"{source_score}/100"
                )

            with col3:
                st.metric(
                    "🛡️ Overall Safety",
                    f"{100 - overall_score}/100"
                )

            st.subheader(
                risk_level
            )

            if risk_score >= 70:
                st.error(
                    "Do not pay money or submit sensitive information "
                    "until this opportunity is independently verified."
                )

            elif risk_score >= 35:
                st.warning(
                    "Verify the company and application source before applying."
                )

            else:
                st.success(
                    "No major scam signals were detected by the current checks."
                )

            st.subheader(
                "🔗 Source Verification"
            )

            st.info(
                source_label
            )

            for reason in source_reasons:
                st.write(
                    reason
                )

            st.subheader(
                "🚨 Risk Analysis"
            )

            if risk_reasons:

                for reason in risk_reasons:
                    st.write(
                        reason
                    )

            else:

                st.success(
                    "No obvious scam indicators were detected."
                )

            st.caption(
                "This is an automated risk assessment, not a guarantee "
                "that the employer or job is legitimate."
            )

            if url:

                if st.button(
                    "📋 Save This Opportunity"
                ):

                    save_application(
                        st.session_state.user_id,
                        company,
                        role,
                        url,
                        "Saved",
                        risk_score,
                        risk_level
                    )

                    st.success(
                        "Opportunity saved."
                    )


# ================================================================
# 4. FAKE JOB DETECTOR
# ================================================================

elif page == "🚨 Fake Job Detector":

    st.header("🚨 Fake Job / Scam Detector")

    st.write(
        "Paste the job advertisement, recruiter message or internship "
        "description below."
    )

    company = st.text_input(
        "Company",
        key="fake_company"
    )

    role = st.text_input(
        "Role",
        key="fake_role"
    )

    salary = st.text_input(
        "Salary / Stipend",
        key="fake_salary"
    )

    url = st.text_input(
        "Application / Recruiter URL",
        key="fake_url"
    )

    message = st.text_area(
        "Job Advertisement / Recruiter Message",
        height=300
    )

    if st.button(
        "🚨 Scan for Fake Job Signals",
        use_container_width=True
    ):

        score, level, reasons = analyze_job(
            company,
            role,
            message,
            salary,
            url
        )

        st.subheader(
            level
        )

        st.metric(
            "Scam Risk Score",
            f"{score}/100"
        )

        st.progress(
            score / 100
        )

        st.subheader(
            "🔍 Detected Signals"
        )

        if reasons:

            for reason in reasons:
                st.write(
                    reason
                )

        else:

            st.success(
                "No obvious scam indicators were detected."
            )

        st.markdown("---")

        st.subheader(
            "🛡️ Safety Recommendations"
        )

        recommendations = [
            "Never pay a registration fee to obtain a job.",
            "Never share OTPs, UPI PINs, card PINs or banking passwords.",
            "Verify the company through its official website.",
            "Check whether the job exists on the company's official careers page.",
            "Do not trust pressure tactics requiring immediate payment.",
            "Check the application domain carefully.",
            "Do not install unknown software requested by a recruiter."
        ]

        for item in recommendations:
            st.write(
                f"• {item}"
            )


# ================================================================
# 5. OPPORTUNITY DNA
# ================================================================

elif page == "🧬 Opportunity DNA":

    st.header("🧬 Opportunity DNA")

    st.write(
        "Analyze an opportunity across career fit, skill fit and safety."
    )

    company = st.text_input(
        "Company",
        key="dna_company"
    )

    role = st.text_input(
        "Role",
        key="dna_role"
    )

    required_text = st.text_input(
        "Required Skills",
        value="Python, Machine Learning, NLP, Pandas, NumPy"
    )

    your_text = st.text_input(
        "Your Skills",
        value=(
            profile["skills"]
            if profile and profile["skills"]
            else "Python, Java, Machine Learning"
        )
    )

    salary = st.text_input(
        "Salary / Stipend",
        key="dna_salary"
    )

    url = st.text_input(
        "Application URL",
        key="dna_url"
    )

    description = st.text_area(
        "Opportunity Description",
        key="dna_description"
    )

    if st.button(
        "🧬 Generate Opportunity DNA",
        use_container_width=True
    ):

        required = split_skills(
            required_text
        )

        your_skills = split_skills(
            your_text
        )

        skill_score = skill_match(
            your_skills,
            required
        )

        risk_score, risk_level, _ = analyze_job(
            company,
            role,
            description,
            salary,
            url
        )

        source_score, _, _ = verify_job_source(
            company,
            url,
            description
        )

        career_score = 80 if role else 40

        overall = int(
            skill_score * 0.35 +
            career_score * 0.20 +
            source_score * 0.25 +
            (100 - risk_score) * 0.20
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🎯 Skill Fit",
                f"{skill_score}%"
            )

        with col2:
            st.metric(
                "🔗 Source Confidence",
                f"{source_score}%"
            )

        with col3:
            st.metric(
                "🚨 Risk",
                f"{risk_score}%"
            )

        with col4:
            st.metric(
                "🧬 Overall Fit",
                f"{overall}%"
            )

        st.progress(
            overall / 100
        )

        if risk_score >= 70:

            st.error(
                "🔴 High-risk opportunity. Verify independently before applying."
            )

        elif risk_score >= 35:

            st.warning(
                "🟡 Opportunity requires additional verification."
            )

        else:

            st.success(
                "🟢 No major risk signals detected."
            )

        st.subheader(
            "📚 Missing Skills"
        )

        missing = missing_skills(
            your_skills,
            required
        )

        for skill in missing:
            st.write(
                f"• {skill}"
            )


# ================================================================
# 6. SKILL MATCHING
# ================================================================

elif page == "🎯 Skill Matching":

    st.header("🎯 Skill Gap & Career Matching")

    career = st.selectbox(
        "Target Career",
        list(CAREERS.keys())
    )

    default = (
        profile["skills"]
        if profile and profile["skills"]
        else "Python, Java, Machine Learning"
    )

    skills_text = st.text_area(
        "Your Skills",
        value=default
    )

    user_skills = split_skills(
        skills_text
    )

    required = CAREERS[career]

    score = skill_match(
        user_skills,
        required
    )

    st.metric(
        "Career Skill Match",
        f"{score}%"
    )

    st.progress(
        score / 100
    )

    st.subheader(
        "Required Skills"
    )

    missing = missing_skills(
        user_skills,
        required
    )

    for skill in required:

        if skill in missing:
            st.write(
                f"⬜ {skill}"
            )
        else:
            st.write(
                f"✅ {skill}"
            )

    if missing:

        st.warning(
            "Focus on these skills next:"
        )

        for skill in missing:
            st.write(
                f"📚 {skill}"
            )

    else:

        st.success(
            "Your current listed skills cover all requirements."
        )


# ================================================================
# 7. RESUME ANALYZER
# ================================================================

elif page == "📝 Resume Analyzer":

    st.header("📝 Resume Analyzer")

    st.write(
        "Upload a TXT or PDF resume. CareerPilot-X extracts technical "
        "skills and gives improvement suggestions."
    )

    uploaded = st.file_uploader(
        "Upload Resume",
        type=[
            "txt",
            "pdf"
        ]
    )

    resume_text = st.text_area(
        "Or paste your resume text",
        height=300
    )

    if st.button(
        "🔍 Analyze Resume",
        use_container_width=True
    ):

        if uploaded:

            extracted = extract_resume_text(
                uploaded
            )

            if extracted:
                resume_text = extracted

        if not resume_text.strip():

            st.warning(
                "Upload a resume or paste resume text."
            )

        else:

            detected = analyze_resume(
                resume_text
            )

            st.subheader(
                "🧠 Detected Skills"
            )

            if detected:

                for skill in detected:
                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.warning(
                    "No listed technical skills were detected."
                )

            st.subheader(
                "💡 Improvement Suggestions"
            )

            suggestions = [
                "Add measurable project outcomes.",
                "Mention technologies used in every major project.",
                "Include GitHub and LinkedIn links.",
                "Add relevant certifications.",
                "Use concise bullet points.",
                "Tailor the resume to each opportunity.",
                "Add internship and hackathon experience.",
                "Highlight AI/ML projects with clear results."
            ]

            for item in suggestions:
                st.write(
                    f"• {item}"
                )


# ================================================================
# 8. CAREER MISSION
# ================================================================

elif page == "🚀 Career Mission":

    st.header("🚀 Career Mission")

    career = st.selectbox(
        "Choose your target career",
        list(CAREERS.keys())
    )

    current_skills = split_skills(
        profile["skills"]
        if profile and profile["skills"]
        else "Python"
    )

    required = CAREERS[career]

    missing = missing_skills(
        current_skills,
        required
    )

    st.subheader(
        f"🎯 Mission: Become a {career}"
    )

    steps = [
        "Complete your student profile.",
        "Build strong fundamentals.",
        "Develop missing technical skills.",
        "Build at least one relevant project.",
        "Improve your resume.",
        "Create/update GitHub portfolio.",
        "Prepare for technical interviews.",
        "Find and verify suitable opportunities.",
        "Apply only after checking the opportunity.",
        "Track your applications."
    ]

    for index, step in enumerate(
        steps,
        start=1
    ):

        st.checkbox(
            f"{index}. {step}",
            key=f"mission_{career}_{index}"
        )

    if missing:

        st.subheader(
            "📚 Your Current Skill Mission"
        )

        for skill in missing:
            st.write(
                f"➡️ Learn **{skill}**"
            )

    else:

        st.success(
            "Your listed skills cover the current career requirements."
        )


# ================================================================
# 9. CAREER DIGITAL TWIN
# ================================================================

elif page == "🧬 Career Digital Twin":

    st.header("🧬 Career Digital Twin")

    if not profile:

        st.warning(
            "Complete your Student Profile first."
        )

    else:

        skills = split_skills(
            profile["skills"]
        )

        projects = [
            x.strip()
            for x in
            (profile["projects"] or "").splitlines()
            if x.strip()
        ]

        certifications = [
            x.strip()
            for x in
            (profile["certifications"] or "").splitlines()
            if x.strip()
        ]

        target = (
            profile["target_career"]
            or "AI/ML Engineer"
        )

        readiness = min(
            100,
            len(skills) * 6
            + len(projects) * 8
            + len(certifications) * 5
            + 15
        )

        st.success(
            "Career Digital Twin generated."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Skills",
                len(skills)
            )

        with col2:
            st.metric(
                "Projects",
                len(projects)
            )

        with col3:
            st.metric(
                "Certifications",
                len(certifications)
            )

        with col4:
            st.metric(
                "Readiness",
                f"{readiness}%"
            )

        st.subheader(
            "👤 Digital Career Profile"
        )

        st.write(
            f"**Target Career:** {target}"
        )

        st.write(
            f"**Education:** {profile['education']}"
        )

        st.write(
            f"**Skills:** {', '.join(skills)}"
        )


# ================================================================
# 10. WHAT-IF CAREER LAB
# ================================================================

elif page == "🔬 What-If Career Lab":

    st.header("🔬 What-If Career Lab")

    career = st.selectbox(
        "Target Career",
        list(CAREERS.keys())
    )

    current_text = st.text_input(
        "Current Skills",
        value=(
            profile["skills"]
            if profile and profile["skills"]
            else "Python, Java, AI, Machine Learning, NLP"
        )
    )

    future_text = st.text_input(
        "Skills You Plan To Learn",
        value="Generative AI, RAG, SQL"
    )

    current = split_skills(
        current_text
    )

    future = split_skills(
        future_text
    )

    required = CAREERS[career]

    current_score = skill_match(
        current,
        required
    )

    future_score = skill_match(
        current + future,
        required
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Match",
            f"{current_score}%"
        )

        st.progress(
            current_score / 100
        )

    with col2:

        st.metric(
            "Future Match",
            f"{future_score}%",
            delta=f"{future_score-current_score}%"
        )

        st.progress(
            future_score / 100
        )

    if future_score > current_score:

        st.success(
            "🎉 Learning these skills improves your target-career match."
        )


# ================================================================
# 11. INTERVIEW SIMULATOR
# ================================================================

elif page == "🎤 Interview Simulator":

    st.header("🎤 Interview Simulator")

    career = st.selectbox(
        "Interview Role",
        list(INTERVIEW_QUESTIONS.keys())
    )

    if st.button(
        "🎲 Generate Question",
        use_container_width=True
    ):

        st.session_state.interview_question = random.choice(
            INTERVIEW_QUESTIONS[career]
        )

        st.session_state.interview_score = None

    if st.session_state.interview_question:

        st.subheader(
            "❓ Interview Question"
        )

        st.info(
            st.session_state.interview_question
        )

        answer = st.text_area(
            "Your Answer",
            height=220
        )

        if st.button(
            "📊 Evaluate Answer",
            use_container_width=True
        ):

            score, feedback = evaluate_answer(
                answer
            )

            st.session_state.interview_score = score

            st.metric(
                "Interview Score",
                f"{score}/100"
            )

            for item in feedback:
                st.write(
                    f"💡 {item}"
                )

            st.info(
                "Recommended structure: "
                "Definition → Explanation → Example → Use Case."
            )


# ================================================================
# 12. APPLICATION TRACKING
# ================================================================

elif page == "📋 Application Tracking":

    st.header("📋 Application Tracking")

    st.subheader(
        "➕ Add Application"
    )

    company = st.text_input(
        "Company",
        key="track_company"
    )

    role = st.text_input(
        "Role",
        key="track_role"
    )

    url = st.text_input(
        "Application URL",
        key="track_url"
    )

    status = st.selectbox(
        "Status",
        [
            "Saved",
            "Applied",
            "Interview",
            "Offer",
            "Rejected"
        ]
    )

    notes = st.text_area(
        "Notes",
        key="track_notes"
    )

    if st.button(
        "💾 Save Application",
        use_container_width=True
    ):

        risk, _, _ = analyze_job(
            company,
            role,
            notes,
            "",
            url
        )

        save_application(
            st.session_state.user_id,
            company,
            role,
            url,
            status,
            risk,
            notes
        )

        st.success(
            "Application saved."
        )

    st.markdown("---")

    st.subheader(
        "📊 Your Applications"
    )

    applications = get_applications(
        st.session_state.user_id
    )

    if not applications:

        st.info(
            "No applications tracked yet."
        )

    else:

        for app in applications:

            with st.container():

                col1, col2, col3 = st.columns(
                    [3, 2, 1]
                )

                with col1:

                    st.subheader(
                        f"{app['role']} — {app['company']}"
                    )

                    st.write(
                        f"Status: **{app['status']}**"
                    )

                    if app["url"]:
                        st.write(
                            app["url"]
                        )

                with col2:

                    st.metric(
                        "Risk",
                        f"{app['risk_score']}/100"
                    )

                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{app['id']}"
                    ):

                        delete_application(
                            app["id"],
                            st.session_state.user_id
                        )

                        st.rerun()

                st.markdown("---")


# ================================================================
# 13. SECURITY & PRIVACY CENTER
# ================================================================

elif page == "🛡️ Security & Privacy":

    st.header("🛡️ Security & Privacy Center")

    st.success(
        "🔐 Account session is active."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Authentication",
            "ACTIVE"
        )

    with col2:

        st.metric(
            "Password Storage",
            "HASHED"
        )

    with col3:

        st.metric(
            "Profile Access",
            "PRIVATE"
        )

    st.markdown("---")

    st.subheader(
        "🔒 Security Protections"
    )

    protections = [
        (
            "Password Hashing",
            "Passwords are stored as cryptographic hashes."
        ),
        (
            "Private Profiles",
            "Profile queries are restricted to the logged-in user."
        ),
        (
            "Session Authentication",
            "Application pages require an authenticated session."
        ),
        (
            "SQL Parameterization",
            "Database queries use parameterized values."
        ),
        (
            "No Colab Storage",
            "The application does not depend on /content."
        ),
        (
            "Sensitive Data Warning",
            "The app warns users not to submit banking credentials or OTPs."
        ),
        (
            "Job Risk Analysis",
            "Potentially suspicious opportunities receive risk warnings."
        ),
        (
            "Source Analysis",
            "Application URLs can be evaluated for source confidence."
        )
    ]

    for title, description in protections:

        st.markdown(
            f"""
            <div class="security-card">
                <b>🟢 {title}</b><br>
                {description}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader(
        "🚫 Never Submit These"
    )

    sensitive = [
        "OTP / One-Time Password",
        "UPI PIN",
        "ATM PIN",
        "Banking password",
        "Credit/debit card PIN",
        "CVV",
        "Authentication tokens",
        "Private API keys"
    ]

    for item in sensitive:

        st.write(
            f"❌ {item}"
        )

    st.markdown("---")

    st.subheader(
        "🛡️ Job Safety Rules"
    )

    rules = [
        "Never pay money to receive a job.",
        "Verify employers through official websites.",
        "Use official career pages whenever possible.",
        "Be careful with shortened URLs.",
        "Do not send OTPs to recruiters.",
        "Do not install unknown software requested by recruiters.",
        "Be suspicious of extremely high compensation with no requirements.",
        "Do not let urgency pressure you into sharing sensitive information."
    ]

    for rule in rules:

        st.write(
            f"• {rule}"
        )

    st.markdown("---")

    st.subheader(
        "👤 Account"
    )

    st.write(
        f"Username: `{st.session_state.username}`"
    )

    st.write(
        f"Email: `{st.session_state.email}`"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()


# ================================================================
# FOOTER
# ================================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; opacity:0.65;">
        🚀 CareerPilot-X 2.0<br>
        AI Career Intelligence • Opportunity Safety • Career Growth
    </div>
    """,
    unsafe_allow_html=True
)
