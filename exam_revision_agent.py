# exam_revision_agent.py (Enhanced with User Profiles + Export)

import os
import json
import markdown2
import pdfkit
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Session Directory
SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

# Global Session State
session_state = {
    "user_id": "default_user",
    "subject": None,
    "topics": [],
    "days": None,
    "focus": []
}

# Style print
def styled(msg, style="info"):
    emojis = {"info": "🧠", "success": "✅", "warning": "⚠️", "error": "❌", "prompt": "📣"}
    print(f"{emojis.get(style, '')} {msg}")

# File path by user
def get_session_path(user_id):
    return os.path.join(SESSION_DIR, f"{user_id}.json")

# Load user session
def load_session():
    session_file = get_session_path(session_state["user_id"])
    if os.path.exists(session_file):
        try:
            with open(session_file, "r") as f:
                session_state.update(json.load(f))
            styled("Previous session loaded.", "success")
        except Exception as e:
            styled(f"Error loading session: {e}", "error")

# Save user session
def save_session():
    try:
        with open(get_session_path(session_state["user_id"]), "w") as f:
            json.dump(session_state, f, indent=2)
    except Exception as e:
        styled(f"Failed to save session: {e}", "error")

# Clear session
def reset_session():
    global session_state
    session_state = {"user_id": session_state["user_id"], "subject": None, "topics": [], "days": None, "focus": []}
    os.remove(get_session_path(session_state["user_id"])) if os.path.exists(get_session_path(session_state["user_id"])) else None
    styled("Session reset.", "success")

# Parse user input
def extract_user_intent(user_input):
    prompt = f'''
    Extract the subject, topics (if any), number of days left to revise, and focus areas
    from the following student input:
    "{user_input}"

    Respond ONLY in this JSON format:
    {{
        "subject": "string",
        "topics": ["list", "of", "topics"],
        "days": int,
        "focus": ["list", "of", "focus areas"]
    }}
    '''
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        styled(f"Failed to extract intent: {e}", "error")
        return {}

# Update session
def update_session_state(parsed):
    if parsed.get("subject"): session_state["subject"] = parsed["subject"]
    if parsed.get("topics"): session_state["topics"] = parsed["topics"]
    if parsed.get("days"): session_state["days"] = parsed["days"]
    if parsed.get("focus"): session_state["focus"] = parsed["focus"]
    save_session()

# Generate plan
def generate_plan():
    context = f'''
The student is preparing for {session_state['subject']}.
Topics: {session_state['topics']}
Focus areas: {session_state['focus']}
Days available: {session_state['days']}

Format the study plan in Markdown with:
- Clear headings and bullet points
- Emojis and motivational tone
- Day-wise tasks for each day
- A friendly message at the end to keep the student motivated
'''
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful study coach."},
                {"role": "user", "content": context}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        styled(f"Failed to generate plan: {e}", "error")
        return "Error generating plan."


# Export plan

def export_markdown(plan, filename="study_plan.md"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(plan)
        styled(f"Markdown exported as {filename}", "success")
    except Exception as e:
        styled(f"Markdown export failed: {e}", "error")

def export_pdf(plan, filename="study_plan.pdf"):
    try:
        html = markdown2.markdown(plan)
        pdfkit.from_string(html, filename)
        styled(f"PDF exported as {filename}", "success")
    except Exception as e:
        styled(f"PDF export failed: {e}", "error")

# CLI session display and edit

def display_session():
    print("\n📌 Current Session:")
    print(json.dumps(session_state, indent=2))

def edit_session():
    while True:
        display_session()
        print("\n💡 Edit Menu:")
        print("1. Subject\n2. Topics\n3. Days\n4. Focus\n5. Back")
        c = input("Choose field to edit (1-5): ").strip()
        if c == "1": session_state["subject"] = input("Subject: ").strip()
        elif c == "2": session_state["topics"] = input("Topics (comma): ").split(",")
        elif c == "3": session_state["days"] = int(input("Days: "))
        elif c == "4": session_state["focus"] = input("Focus areas (comma): ").split(",")
        elif c == "5": break
        else: continue
        save_session()
        styled("Session updated!", "success")

# User selection

def select_user():
    styled("Enter your name to start or continue your session.", "prompt")
    uid = input("Your Name: ").strip().lower().replace(" ", "_")
    session_state["user_id"] = uid
    load_session()

# Main agent

def run_agent():
    while True:
        print("\n📚 Revision Coach Menu")
        print("1. New revision input\n2. View session\n3. Edit session\n4. Generate plan\n5. Export to Markdown/PDF\n6. Reset session\n7. Exit")
        c = input("Choose (1-7): ").strip()

        if c == "1":
            u = input("Describe your revision goal: ")
            if not u: continue
            p = extract_user_intent(u)
            if p: update_session_state(p)
        elif c == "2":
            display_session()
        elif c == "3":
            edit_session()
        elif c == "4":
            if not session_state['subject'] or not session_state['days']:
                styled("Session incomplete.", "warning")
                continue
            print("\n📝 Your Revision Plan:\n")
            print(generate_plan())
        elif c == "5":
            plan = generate_plan()
            export_markdown(plan)
            export_pdf(plan)
        elif c == "6":
            reset_session()
        elif c == "7":
            styled("Goodbye! Come back soon.", "info")
            break
        else:
            styled("Invalid option.", "warning")

if __name__ == "__main__":
    select_user()
    run_agent()
