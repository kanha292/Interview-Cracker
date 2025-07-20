from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# --- CONFIG ---
API_KEY = "AIzaSyA-Uw8bI-bT-ceQR-0sN3c6geFceOElKPM"  # Replace with your actual API key
MODEL_NAME = "models/gemini-1.5-flash"

# --- INITIALIZE ---
app = Flask(__name__, template_folder="templates")

# --- SETUP GEMINI ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name=MODEL_NAME)
except Exception as config_err:
    print(f"[ERROR] Gemini config failed: {config_err}")
    model = None

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    if not model:
        return jsonify({"error": "Gemini model not initialized."}), 500

    data = request.get_json()
    question = data.get("original", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    prompt = f"""
You are acting as an expert AI assistant in a **cybersecurity job interview**.

The user is being asked a question by the interviewer. Your job is to:
- Provide a highly accurate, professional, and concise answer.
- The answer must be suitable to **speak directly during the interview**.
- Do not include explanations or extra content — just the best answer.

Interview Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text.strip()})
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500


# --- RUN ---
if __name__ == "__main__":
    app.run(debug=True)
