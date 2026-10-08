# ================================================================
# 🚀 CAREERPILOT-X 2.0
# AI Career Guidance + Interview Simulator
# Render Ready Version
# ================================================================

import os
import random
import re
from pathlib import Path

import streamlit as st

# ================================================================
# PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="CareerPilot-X 2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# SAFE PROJECT DIRECTORY
# ================================================================
# IMPORTANT:
# Do NOT use /content here.
# /content is a Google Colab directory and causes PermissionError
# on Render.
#
# Render allows the application directory and /tmp for temporary data.

PROJECT_DIR = Path(os.environ.get("PROJECT_DIR", "/tmp/careerpilot_x"))

try:
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    PROJECT_DIR = Path("/tmp/careerpilot_x")
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

# ================================================================
# CUSTOM CSS
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
        opacity: 0.8;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 15px;
    }

    .risk-high {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(255, 80, 80, 0.15);
    }

    .risk-medium {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(255, 180, 50, 0.15);
    }

    .risk-low {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(50, 200, 100, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ================================================================
# HEADER
# ================================================================

st.markdown(
    '<div class="main-title">🚀 CareerPilot-X 2.0</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Career Guidance, Skill Analysis & Interview Simulator'
    '</div>',
    unsafe_allow_html=True
)

# ================================================================
# SESSION STATE
# ================================================================

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "interview_question" not in st.session_state:
    st.session_state.interview_question = None

if "interview_score" not in st.session_state:
    st.session_state.interview_score = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# ================================================================
# CAREER DATA
# ================================================================

CAREERS = {
    "AI/ML Engineer": {
        "skills": [
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
        "description":
            "Build and deploy machine learning and artificial intelligence systems."
    },

    "Data Scientist": {
        "skills": [
            "Python",
            "Statistics",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "SQL",
            "Data Visualization"
        ],
        "description":
            "Analyze data and build predictive models to solve business problems."
    },

    "Data Analyst": {
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Power BI",
            "Data Visualization"
        ],
        "description":
            "Transform raw data into useful insights and reports."
    },

    "Software Developer": {
        "skills": [
            "Python",
            "Java",
            "Data Structures",
            "Algorithms",
            "OOP",
            "Git",
            "SQL"
        ],
        "description":
            "Design, develop and maintain software applications."
    },

    "Generative AI Engineer": {
        "skills": [
            "Python",
            "Generative AI",
            "LLMs",
            "Prompt Engineering",
            "RAG",
            "NLP",
            "Vector Databases"
        ],
        "description":
            "Build applications using large language models and generative AI."
    },

    "Cybersecurity Analyst": {
        "skills": [
            "Networking",
            "Linux",
            "Cybersecurity",
            "Python",
            "Ethical Hacking",
            "Security Tools"
        ],
        "description":
            "Protect systems, networks and applications from cyber threats."
    },

    "Cloud Engineer": {
        "skills": [
            "Linux",
            "Networking",
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes"
        ],
        "description":
            "Build, deploy and maintain cloud infrastructure."
    },

    "DevOps Engineer": {
        "skills": [
            "Linux",
            "Git",
            "Docker",
            "Kubernetes",
            "CI/CD",
            "AWS"
        ],
        "description":
            "Automate software development, deployment and infrastructure."
    },

    "NLP Engineer": {
        "skills": [
            "Python",
            "NLP",
            "Machine Learning",
            "Deep Learning",
            "Transformers",
            "LLMs"
        ],
        "description":
            "Develop systems that understand and process human language."
    },

    "AI Product Manager": {
        "skills": [
            "AI Fundamentals",
            "Product Management",
            "Communication",
            "Analytics",
            "User Research",
            "Business Strategy"
        ],
        "description":
            "Manage AI products from idea to development and launch."
    }
}

# ================================================================
# INTERVIEW QUESTIONS
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
        "What is a training dataset?",
        "What is model evaluation?",
        "What is cross-validation?"
    ],

    "Data Scientist": [
        "What is the difference between mean and median?",
        "What is data preprocessing?",
        "What is feature engineering?",
        "What is overfitting?",
        "What is regression?",
        "What is classification?",
        "What is cross-validation?",
        "What is exploratory data analysis?"
    ],

    "Data Analyst": [
        "What is data analysis?",
        "What is SQL?",
        "What is a database?",
        "What is data visualization?",
        "What is the difference between mean and median?",
        "What is an SQL JOIN?"
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

    "Generative AI Engineer": [
        "What is Generative AI?",
        "What is an LLM?",
        "What is prompt engineering?",
        "What is RAG?",
        "What is a vector database?",
        "What is hallucination in AI?",
        "How can RAG reduce hallucinations?"
    ],

    "Cybersecurity Analyst": [
        "What is cybersecurity?",
        "What is phishing?",
        "What is malware?",
        "What is a firewall?",
        "What is encryption?",
        "What is authentication?"
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
# HELPER FUNCTIONS
# ================================================================

def normalize_skill(skill):
    """Normalize a skill for comparison."""
    return re.sub(r"[^a-z0-9+#]", "", skill.lower())


def calculate_skill_match(user_skills, required_skills):
    """Calculate percentage of required skills matched."""

    user_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    required_normalized = {
        normalize_skill(skill)
        for skill in required_skills
    }

    if not required_normalized:
        return 0

    matched = user_normalized.intersection(required_normalized)

    return round(
        (len(matched) / len(required_normalized)) * 100,
        2
    )


def get_missing_skills(user_skills, required_skills):
    """Return missing skills."""

    user_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    return [
        skill
        for skill in required_skills
        if normalize_skill(skill) not in user_normalized
    ]


def evaluate_answer(answer, question):
    """
    Simple interview-answer evaluator.

    This intentionally avoids requiring an external AI API,
    making the application stable on Render.
    """

    if not answer.strip():
        return 0, "No answer provided."

    answer_words = answer.lower().split()

    technical_keywords = [
        "machine",
        "learning",
        "model",
        "data",
        "algorithm",
        "python",
        "training",
        "testing",
        "feature",
        "prediction",
        "accuracy",
        "deep",
        "neural",
        "language",
        "ai",
        "generative",
        "llm",
        "rag",
        "deployment",
        "overfitting"
    ]

    keyword_count = sum(
        1 for word in technical_keywords
        if word in answer_words
    )

    length_score = min(len(answer_words) / 30, 1)

    score = min(
        100,
        int(
            keyword_count * 8 +
            length_score * 40
        )
    )

    if score >= 70:
        feedback = "Strong answer. Try adding a real-world example to make it even better."

    elif score >= 40:
        feedback = "Good start. Add more technical details and an example."

    else:
        feedback = "Try explaining the concept more clearly with key technical points."

    return score, feedback


# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("🧭 CareerPilot-X")

page = st.sidebar.radio(
    "Choose a module",
    [
        "🏠 Career Dashboard",
        "🎯 Skill Gap Analyzer",
        "📝 Resume Analyzer",
        "🎤 Interview Simulator",
        "🧬 Career Digital Twin",
        "🔬 What-If Career Lab",
        "🧬 Opportunity DNA",
        "📋 Application Checklist"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "CareerPilot-X 2.0 helps students discover careers, "
    "identify skill gaps and prepare for interviews."
)

# ================================================================
# 1. CAREER DASHBOARD
# ================================================================

if page == "🏠 Career Dashboard":

    st.header("🏠 Career Dashboard")

    st.write(
        "Enter your current skills and let CareerPilot-X "
        "identify suitable career paths."
    )

    default_skills = [
        "Python",
        "Java",
        "AI",
        "Machine Learning",
        "NLP"
    ]

    skills_text = st.text_input(
        "Your skills",
        value=", ".join(default_skills),
        placeholder="Python, Java, Machine Learning..."
    )

    user_skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    if st.button("🚀 Analyze My Career", use_container_width=True):

        results = []

        for career, data in CAREERS.items():

            match = calculate_skill_match(
                user_skills,
                data["skills"]
            )

            results.append(
                (career, match, data["description"])
            )

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        st.success("Career analysis completed!")

        for career, match, description in results:

            with st.container():

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(career)
                    st.write(description)

                with col2:
                    st.metric(
                        "Skill Match",
                        f"{match}%"
                    )

                st.progress(
                    min(match / 100, 1.0)
                )

                st.markdown("---")


# ================================================================
# 2. SKILL GAP ANALYZER
# ================================================================

elif page == "🎯 Skill Gap Analyzer":

    st.header("🎯 Skill Gap Analyzer")

    career = st.selectbox(
        "Choose your target career",
        list(CAREERS.keys())
    )

    skills_text = st.text_input(
        "Enter your current skills",
        value="Python, Java, AI, Machine Learning"
    )

    user_skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    required = CAREERS[career]["skills"]

    match = calculate_skill_match(
        user_skills,
        required
    )

    missing = get_missing_skills(
        user_skills,
        required
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Skill Match",
            f"{match}%"
        )

    with col2:
        st.metric(
            "Missing Skills",
            len(missing)
        )

    st.progress(
        min(match / 100, 1.0)
    )

    st.subheader("✅ Required Skills")

    for skill in required:
        if skill in missing:
            st.write(f"⬜ {skill}")
        else:
            st.write(f"✅ {skill}")

    if missing:

        st.subheader("📚 Recommended Learning")

        for skill in missing:
            st.write(
                f"• Learn **{skill}**"
            )

    else:

        st.success(
            "Excellent! You currently match all the listed skills."
        )


# ================================================================
# 3. RESUME ANALYZER
# ================================================================

elif page == "📝 Resume Analyzer":

    st.header("📝 Resume Analyzer")

    st.write(
        "Paste your resume text below. CareerPilot-X will "
        "identify technical skills and provide improvement suggestions."
    )

    resume_text = st.text_area(
        "Paste resume text",
        height=300
    )

    if st.button(
        "🔍 Analyze Resume",
        use_container_width=True
    ):

        if not resume_text.strip():

            st.warning(
                "Please paste your resume text first."
            )

        else:

            all_skills = set()

            for data in CAREERS.values():
                all_skills.update(data["skills"])

            detected = []

            for skill in all_skills:

                if skill.lower() in resume_text.lower():
                    detected.append(skill)

            st.subheader("🧠 Detected Skills")

            if detected:

                for skill in sorted(detected):
                    st.write(f"✅ {skill}")

            else:

                st.warning(
                    "No major technical skills were detected."
                )

            st.subheader("💡 Resume Suggestions")

            suggestions = [
                "Add measurable project results.",
                "Mention technologies used in projects.",
                "Include GitHub and LinkedIn links.",
                "Add relevant certifications.",
                "Use strong action verbs.",
                "Keep project descriptions concise."
            ]

            for suggestion in suggestions:
                st.write(f"• {suggestion}")


# ================================================================
# 4. INTERVIEW SIMULATOR
# ================================================================

elif page == "🎤 Interview Simulator":

    st.header("🎤 AI Interview Simulator")

    career = st.selectbox(
        "Select interview role",
        list(INTERVIEW_QUESTIONS.keys())
    )

    st.write(
        "Practice technical interview questions and "
        "receive instant feedback."
    )

    if st.button(
        "🎲 Generate Interview Question",
        use_container_width=True
    ):

        question = random.choice(
            INTERVIEW_QUESTIONS[career]
        )

        st.session_state.interview_question = question
        st.session_state.interview_started = True

    if st.session_state.interview_started:

        question = st.session_state.interview_question

        st.subheader("❓ Interview Question")

        st.info(question)

        answer = st.text_area(
            "Your answer",
            height=180,
            key="current_answer"
        )

        if st.button(
            "📊 Evaluate My Answer",
            use_container_width=True
        ):

            score, feedback = evaluate_answer(
                answer,
                question
            )

            st.session_state.interview_score = score

            st.metric(
                "Interview Score",
                f"{score}/100"
            )

            if score >= 70:
                st.success(feedback)

            elif score >= 40:
                st.warning(feedback)

            else:
                st.error(feedback)

            st.subheader("💡 Interview Tip")

            st.write(
                "Use the structure: **Definition → Explanation → "
                "Example → Real-world use case**."
            )


# ================================================================
# 5. CAREER DIGITAL TWIN
# ================================================================

elif page == "🧬 Career Digital Twin":

    st.header("🧬 Career Digital Twin")

    st.write(
        "Create a simple digital representation of your "
        "current career profile."
    )

    name = st.text_input(
        "Your name"
    )

    education = st.text_input(
        "Education",
        value="BTech CSE-AIML"
    )

    skills = st.text_input(
        "Skills",
        value="Python, Java, AI, Machine Learning, NLP"
    )

    projects = st.number_input(
        "Number of AI/ML projects",
        min_value=0,
        max_value=100,
        value=6
    )

    internship = st.checkbox(
        "Completed an internship"
    )

    if st.button(
        "🧬 Generate Digital Twin",
        use_container_width=True
    ):

        skill_list = [
            x.strip()
            for x in skills.split(",")
            if x.strip()
        ]

        readiness = min(
            100,
            len(skill_list) * 8 +
            projects * 5 +
            (15 if internship else 0)
        )

        st.success(
            "Career Digital Twin generated!"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Skills",
                len(skill_list)
            )

        with col2:
            st.metric(
                "Projects",
                projects
            )

        with col3:
            st.metric(
                "Career Readiness",
                f"{readiness}%"
            )

        st.subheader("👤 Profile")

        st.write(
            f"**Name:** {name or 'Student'}"
        )

        st.write(
            f"**Education:** {education}"
        )

        st.write(
            f"**Skills:** {', '.join(skill_list)}"
        )


# ================================================================
# 6. WHAT-IF CAREER LAB
# ================================================================

elif page == "🔬 What-If Career Lab":

    st.header("🔬 What-If Career Lab")

    st.write(
        "See how adding new skills can improve your "
        "career readiness."
    )

    career = st.selectbox(
        "Target Career",
        list(CAREERS.keys())
    )

    current_skills_text = st.text_input(
        "Current skills",
        value="Python, Java, AI, Machine Learning, NLP"
    )

    additional_skills_text = st.text_input(
        "Skills you plan to learn",
        value="Generative AI, RAG, SQL"
    )

    current_skills = [
        x.strip()
        for x in current_skills_text.split(",")
        if x.strip()
    ]

    additional_skills = [
        x.strip()
        for x in additional_skills_text.split(",")
        if x.strip()
    ]

    required = CAREERS[career]["skills"]

    current_match = calculate_skill_match(
        current_skills,
        required
    )

    future_match = calculate_skill_match(
        current_skills + additional_skills,
        required
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Match",
            f"{current_match}%"
        )

    with col2:
        st.metric(
            "Future Match",
            f"{future_match}%",
            delta=f"{future_match - current_match:.1f}%"
        )

    st.subheader("📈 Career Improvement")

    st.progress(
        min(future_match / 100, 1.0)
    )

    if future_match > current_match:
        st.success(
            "These additional skills improve your career match."
        )


# ================================================================
# 7. OPPORTUNITY DNA
# ================================================================

elif page == "🧬 Opportunity DNA":

    st.header("🧬 Opportunity DNA")

    st.write(
        "Analyze how well your profile fits a hypothetical "
        "career opportunity."
    )

    job_title = st.text_input(
        "Opportunity title",
        value="AI/ML Intern"
    )

    required_skills_text = st.text_input(
        "Required skills",
        value="Python, Machine Learning, NLP, Pandas, NumPy"
    )

    candidate_skills_text = st.text_input(
        "Your skills",
        value="Python, Machine Learning, NLP, Java"
    )

    required_skills = [
        x.strip()
        for x in required_skills_text.split(",")
        if x.strip()
    ]

    candidate_skills = [
        x.strip()
        for x in candidate_skills_text.split(",")
        if x.strip()
    ]

    match = calculate_skill_match(
        candidate_skills,
        required_skills
    )

    missing = get_missing_skills(
        candidate_skills,
        required_skills
    )

    if st.button(
        "🧬 Analyze Opportunity",
        use_container_width=True
    ):

        st.subheader(
            f"🎯 {job_title}"
        )

        st.metric(
            "Opportunity Match",
            f"{match}%"
        )

        st.progress(
            min(match / 100, 1.0)
        )

        if missing:

            st.subheader(
                "⚠️ Missing Skills"
            )

            for skill in missing:
                st.write(f"• {skill}")

        else:

            st.success(
                "Your profile matches all listed requirements."
            )


# ================================================================
# 8. APPLICATION CHECKLIST
# ================================================================

elif page == "📋 Application Checklist":

    st.header("📋 Internship / Job Application Checklist")

    st.write(
        "Use this checklist before submitting an application."
    )

    checklist_items = [
        "Resume updated",
        "GitHub profile updated",
        "LinkedIn profile updated",
        "Projects uploaded",
        "Project README completed",
        "Portfolio website ready",
        "Relevant skills added",
        "Cover letter prepared",
        "Interview preparation completed",
        "Application submitted"
    ]

    completed = 0

    for item in checklist_items:

        if st.checkbox(item):
            completed += 1

    progress = completed / len(checklist_items)

    st.progress(progress)

    st.metric(
        "Application Readiness",
        f"{int(progress * 100)}%"
    )

    if completed == len(checklist_items):

        st.success(
            "🎉 Everything is ready. Good luck with your application!"
        )

    elif completed >= 7:

        st.info(
            "Almost ready! Complete the remaining checklist items."
        )

    else:

        st.warning(
            "Complete more preparation steps before applying."
        )


# ================================================================
# FOOTER
# ================================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; opacity:0.7;">
        🚀 CareerPilot-X 2.0 |
        AI-Powered Career Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)
