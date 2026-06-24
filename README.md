# 🤝 MannMitra

**MannMitra** is a student-first digital mental health and psychological support ecosystem designed to provide AI-powered self-help tools, confidential counseling access, peer forums, and institutional dashboards.

🌐 **Deployed App**: [https://mann-mitra.onrender.com](https://mann-mitra.onrender.com) *(Update this link once your deployment completes!)*

---

## 🚀 Core Features

### 1. 🤖 AI-Powered Self-Help Tools
* **24×7 Chatbot**: An interactive, Gemini-powered chatbot that listens, guides, and screens for mental health issues.
* **Mood Tracking**: Help students monitor their emotional health over time.
* **Gamified Screening**: Engaging, stigma-free wellness checks based on clinical standards (e.g., PHQ-9, GAD-7).

### 2. 🔒 Confidential Counseling Access
* **Anonymous Booking**: Connect securely and anonymously with college or university counselors.
* **Instant Helpline**: Quick access to helpline contacts for urgent support.

### 3. 👥 Peer & Community Support
* **Community Forum**: An anonymous space for students to share experiences, support each other, and discuss mental health.
* **Resource Hub**: Access to curated files, wellness exercises, and mental health content.

### 4. 📊 Institutional & Policy Integration
* **College/University Dashboards**: Visual analytics that help administrators monitor campus-wide student wellbeing and identify early risks safely.
* **Policy Models**: Supports counselor-to-student ratios, policy alignment, and administrative outreach.

---

## 🛠️ Tech Stack

* **Backend**: Python / Django (v5.2.x)
* **Frontend**: HTML5, Vanilla CSS, JavaScript
* **Database**: SQLite (Local Dev) / PostgreSQL (Production) via `dj-database-url`
* **Authentication**: Supabase API / JWT Backend Integration
* **AI Engine**: Google Gemini API (`gemini-2.5-flash`)
* **Static Assets**: WhiteNoise (Asset compression and hosting)
* **Production Web Server**: Gunicorn

---

## 📁 Project Directory Structure

Here is a visual map of the key directories and files in this project:

```text
Mann-Mitra/
├── build.sh                  # Render shell build script
├── Procfile                  # Production start command (Gunicorn)
├── requirements.txt          # Python project dependencies
├── db.sqlite3                # Local development SQLite database (ignored by Git)
├── mindease/                 # Django Main Configuration folder
│   ├── settings.py           # Core settings (Supabase, Gemini, WhiteNoise, DB)
│   ├── urls.py               # Application-wide routing configurations
│   ├── wsgi.py               # WSGI entrypoint for production servers
│   └── asgi.py               # ASGI entrypoint
├── core/                     # Main App containing the business logic
│   ├── views.py              # Page controllers, AI chat engine, and dashboard views
│   ├── models.py             # Django Database models (Users, Analytics, Logs)
│   ├── authentication.py     # Custom Supabase JWT Authentication handler
│   ├── static/               # Local static assets (CSS, Images, Javascript)
│   └── templates/            # HTML views
│       ├── home.html         # Main landing page
│       ├── chatbot.html      # AI Chatbot interface
│       ├── community.html    # Peer-to-peer discussion forum
│       ├── booking.html      # Anonymous counselor booking page
│       ├── screening.html    # Gamified PHQ-9/GAD-7 tests
│       ├── StudentDashboard/ # Student-focused view pages
│       ├── InstDashboard/    # Campus admin analytics and alert settings
│       └── AdminDashboard/   # Main platform control templates
└── staticfiles/              # Directory where production static assets are compiled
```

---

## 💻 Local Setup Instructions

Follow these steps to run the project locally on your machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kritisp/MannMitra.git
   cd Mann-Mitra
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add the following parameters:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   SUPABASE_URL=https://bfovpyytilvygcwttgxu.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.5-flash
   ```

5. **Run Migrations & Start the Server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## ☁️ Deployment on Render

This project is pre-configured for a smooth Render deployment. Refer to the internal documentation or setup guides to configure your **Web Service** using `./build.sh` as the Build Command and `gunicorn mindease.wsgi:application` as the Start Command.
