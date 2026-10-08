# 🚀 CareerPilot-X 2.0

### AI-Powered Career Operating System for Students

CareerPilot-X 2.0 is an AI-powered career guidance platform designed to help students move from **career discovery to job application and interview preparation** in one place.

It analyzes a student's skills, projects, experience, and career interests to provide personalized career recommendations, identify skill gaps, generate learning roadmaps, analyze resumes, find real-time job opportunities, simulate interviews, and track applications.

---

## 🎯 Project Vision

**CareerPilot-X 2.0** aims to become an **AI Career Operating System** that guides students through the complete career journey:

> **Discover → Analyze → Learn → Prepare → Apply → Track → Improve**

Instead of using separate tools for career selection, skill analysis, job searching, resume checking, and interview preparation, CareerPilot-X 2.0 brings these capabilities together in one platform.

---

## ✨ Key Features

### 👤 1. Student Dashboard
View your career profile, skills, projects, experience, readiness score, and recommended career.

### 🎯 2. Career Match
Compares your current skills with multiple career paths and calculates a career-match percentage.

Supported career paths include:

- AI/ML Engineer
- Data Scientist
- Data Analyst
- Software Developer
- Web Developer
- Cybersecurity Analyst
- Cloud Engineer
- DevOps Engineer
- Business Analyst
- UI/UX Designer

### 🧩 3. Skill Gap Analysis
Identifies:

- Skills you already have
- Skills you are missing
- Skills required for your target career
- Areas that need improvement

### 🗺️ 4. Personalized Learning Roadmap
Provides a structured roadmap based on the selected career, including technical skills, tools, projects, and preparation areas.

### 🔎 5. Real-Time Job Search
Uses **SerpApi Google Jobs search** to retrieve real job and internship opportunities.

The system attempts to show only opportunities containing:

- Job title
- Company
- Source/apply URL

If salary or deadline information is unavailable, it is shown as **"Not specified"** rather than being invented.

### 🧬 6. Opportunity DNA
Analyzes an opportunity against the student's current skills and shows:

- Matching skills
- Missing skills
- Opportunity fit percentage
- Areas to improve

### 📄 7. Resume Analyzer
Analyzes a resume and provides insights into:

- Resume sections
- Career keywords
- Skill alignment
- Resume score
- Areas for improvement

### 🔮 8. What-If Career Lab
Allows students to experiment with additional skills and see how those skills could affect their career-match score.

Example:

> What if I add SQL, NumPy, Pandas, PyTorch and TensorFlow?

The system recalculates the career match.

### 🪞 9. Career Digital Twin
Creates a career-readiness representation of the student based on:

- Skills
- Projects
- Experience
- Career alignment

### 🎤 10. Interview Simulator
Provides career-specific interview questions and evaluates answers based on response quality and completeness.

### 📊 11. Career Readiness Score
Combines different aspects of the student's profile to estimate overall career readiness.

### ⚖️ 12. Compare Opportunities
Compare job opportunities based on available information and career fit.

### 📋 13. Application Tracker
Track application progress using statuses such as:

- Saved
- Applied
- Assessment
- Interview
- Offer
- Rejected

### ⭐ 14. Saved Opportunities
Keep important job opportunities available for later review.

### 🎯 15. Career Mission
Provides actionable career tasks to help students continuously improve their profile.

### 🧪 16. Full System Test
Runs built-in checks across major CareerPilot-X 2.0 components.

---

## 🧠 How It Works

```text
Student Profile
      ↓
Career Match
      ↓
Skill Gap Analysis
      ↓
Learning Roadmap
      ↓
Resume Analysis
      ↓
Real-Time Job Search
      ↓
Opportunity DNA
      ↓
Interview Preparation
      ↓
Application Tracking
      ↓
Career Progress
```

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Requests**
- **SerpApi**
- **Google Jobs Search**
- **GitHub**
- **Render**

---

## 🔐 Job Search & Trust Approach

CareerPilot-X 2.0 is designed to avoid generating fake job opportunities.

The job-search workflow:

```text
SerpApi
   ↓
Live Job Search
   ↓
Retrieve Listing
   ↓
Check Job Title
   ↓
Check Company
   ↓
Check Source URL
   ↓
Display Opportunity
```

The platform does **not** guarantee that an employer or job listing is legitimate. Users should always verify the employer, listing, and application website before sharing personal information or applying.

If information such as salary or deadline is unavailable, CareerPilot-X 2.0 does not invent it.

---

## 📁 Project Structure

```text
CareerPilot-X-2.0/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/CareerPilot-X-2.0.git
cd CareerPilot-X-2.0
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔑 SerpApi Configuration

CareerPilot-X 2.0 requires a **SerpApi API key** for real-time job searching.

The API key should be entered securely through the application's runtime input.

### ⚠️ Security

**Never upload your API key to GitHub.**

Do not hard-code your key inside:

```text
app.py
```

or any public repository file.

If an API key is accidentally exposed, revoke it and generate a new one.

---

## ☁️ Deployment

CareerPilot-X 2.0 can be deployed using **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 🎓 Target Users

CareerPilot-X 2.0 is designed primarily for:

- College students
- Engineering students
- Freshers
- Beginners entering AI/ML
- Students looking for internships
- Students preparing for placements
- Students unsure which career path to choose

---

## 🌟 Why CareerPilot-X 2.0?

Students often need multiple platforms for:

- Career discovery
- Skill-gap analysis
- Learning
- Resume improvement
- Job searching
- Interview preparation
- Application tracking

CareerPilot-X 2.0 brings these activities together into one career-focused platform.

### One platform. One career journey.

> **Discover your career. Build your skills. Find opportunities. Prepare. Apply. Grow.**

---

## 🚀 Future Improvements

Planned improvements can include:

- AI-powered resume rewriting
- Advanced semantic resume-job matching
- More career paths
- Personalized project recommendations
- Job alerts
- LinkedIn profile analysis
- Interview voice mode
- Advanced AI career coaching
- Skill progress tracking
- Personalized weekly career plans
- More verified job sources

---

## ⚠️ Disclaimer

CareerPilot-X 2.0 provides career guidance and opportunity information for educational and informational purposes.

Career-match scores and readiness scores are estimates based on the information provided by the user and should not be treated as guaranteed predictions.

Always independently verify job listings, employers, application websites, salaries, deadlines, and other opportunity details before making career or financial decisions.

---

## 👩‍💻 Project

**CareerPilot-X 2.0**

An AI-powered career operating system designed to help students navigate their journey from **career discovery to employment readiness**.

---

### ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub and sharing it with other students interested in AI, career development, and technology.
