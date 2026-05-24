# Antigravity AI Code Reviewer

A beautiful, modular, and fast AI Code Reviewer web application built with **Python**, **Streamlit**, and the **Groq API** (powered by the `llama3-70b-8192` model). 

It analyzes source code across multiple categories (bugs, security flaws, performance, readability, and best practices) and provides structured feedback with severity levels, quality scores, and optimized code recommendations.

---

## Features
- **File Upload & Code Pasting**: Drag-and-drop code files or write/paste snippets directly.
- **Language Support**: Default test snippets for Python, JavaScript, Java, C++, and SQL, with general support for any language.
- **Visual Dashboards**:
  - A dynamic SVG-based **Health Score Gauge** displaying the aggregate code quality.
  - An **Issue Severity Distribution** grid showing counts of Critical, Warning, Optimization, and Info problems.
- **Detailed Finding Cards**: Glassmorphic UI cards presenting issue category, description, exact line number, and a suggested resolution.
- **Improved Code Comparison**: Fully optimized code output, side-by-side workspace comparison, copy-to-clipboard, and quick download.
- **Report Exporting**: Generate and download a comprehensive code review report as a formatted Markdown file (`.md`).
- **Session History Log**: Track scores and issue metrics of reviews run in the current session.

---

## Project Structure
```
c:/Users/hasin/OneDrive/Documents/autocode/
├── requirements.txt      # Project library dependencies
├── .env.example          # Environment variables template
├── config.py             # App configurations, constants & templates
├── review_service.py     # Groq API interaction & JSON prompt parser
├── ui_components.py      # Custom CSS animations, cards, badges & SVG gauge
└── app.py                # Main Streamlit web application orchestrator
```

---

## Local Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone/Copy Code
Ensure all the files listed in the project structure are in your desired workspace folder (e.g. `autocode`).

### 3. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a copy of `.env.example` named `.env` and fill in your Groq API Key:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key
```
*Note: You can get your free API key by signing up at the [Groq Console](https://console.groq.com/keys).*

### 5. Run the Web Application
Launch the dev server using Streamlit:
```bash
streamlit run app.py
```
This will open the application in your default web browser (typically at `http://localhost:8501`).

---

## Deployment to Streamlit Cloud

Follow these steps to deploy this application to the web for free using [Streamlit Community Cloud](https://streamlit.io/cloud):

### Step 1: Push to GitHub
Create a repository on GitHub and push the code:
```bash
git init
git add .
git commit -m "Initial commit: AI Code Reviewer"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
*Make sure to add `.env` to your `.gitignore` so your API key is never committed to GitHub!*

### Step 2: Deploy on Streamlit Cloud
1. Log into [Streamlit Share](https://share.streamlit.io/).
2. Click **"New app"** (or **"Create app"**).
3. Select your repository, branch (`main`), and main file path (`app.py`).
4. Click **"Advanced settings"** before deploying.

### Step 3: Add API Secrets
In the **Secrets** text area within Advanced settings, paste your Groq API Key using Streamlit's secrets format:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key"
```
Click **Save**.

### Step 4: Launch
Click **"Deploy!"**. Within a couple of minutes, your application will build, download dependencies from `requirements.txt`, and be live on a public URL. Streamlit will automatically read the secret key and map it to `os.getenv("GROQ_API_KEY")`.
