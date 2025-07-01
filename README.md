# 🧠 Exam Revision Agent

A command-line AI-powered study coach that converts your natural language goals into personalized revision plans — with support for session memory, Markdown/PDF exports, and user profiles. Built using `Groq API` + `LLaMA3`.

---

## ✨ Features

- 🧾 Understands your input (e.g. "I have 5 days to revise Physics optics and waves")
- 💾 Remembers sessions by user name (saved to disk)
- 🗂️ View and edit sessions at any time
- 📆 Generates a Markdown-formatted daily plan
- 📄 Export plans to `.md` and `.pdf` (via `pdfkit`)
- 😄 Supportive tone, emojis, and formatting included

---

## 🛠️ Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/exam-revision-agent.git
cd exam-revision-agent

```
You also need wkhtmltopdf for PDF export to work.
---
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
---

### 3. Set your Groq API key
Create a .env file in the root:
```bash
GROQ_API_KEY=your_groq_api_key
```
---

### 4. Run the agent
```bash
python exam_revision_agent.py
```
📂 Session Storage
Session data is saved in the sessions/ folder as JSON files named after the user (e.g., ritesh.json). This allows returning users to continue from where they left off.

📌 Credits

Built by Ritesh with ❤️ using:

🚀 Groq API — for ultra-fast LLM inference

🧠 LLaMA3 — the model powering study plan generation

📝 markdown2 — for converting Markdown to HTML

📄 pdfkit — for exporting clean PDF study plans
