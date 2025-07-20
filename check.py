# # from flask import Flask, render_template, request, jsonify
# # import google.generativeai as genai
# # from jiwer import wer

# # # --- CONFIG ---
# # API_KEY = "AIzaSyA-Uw8bI-bT-ceQR-0sN3c6geFceOElKPM"
# # MODEL_NAME = "models/gemini-2.0-flash"

# # # --- INITIALIZE APP ---
# # app = Flask(__name__, template_folder='templates')

# # # --- CONFIGURE GEMINI WITH LOW TEMPERATURE ---
# # genai.configure(api_key=API_KEY)
# # model = genai.GenerativeModel(
# #     model_name=MODEL_NAME,
# #     generation_config={
# #         "temperature": 0.2,
# #         "top_p": 1,
# #         "top_k": 1
# #     }
# # )

# # # --- HOME PAGE ---
# # @app.route("/")
# # def index():
# #     return render_template("index.html")

# # # --- ACCURACY CHECK ROUTE ---
# # @app.route("/evaluate", methods=["POST"])
# # def evaluate():
# #     data = request.json
# #     original = data.get("original", "")
# #     generated = data.get("generated", "")

# #     # Manually compute WER using jiwer
# #     try:
# #         calculated_wer = round(wer(original, generated) * 100, 2)  # in percentage
# #     except:
# #         calculated_wer = "Error calculating WER"

# #     # Prompt Gemini to find errors only (not calculate WER)
# #     prompt = f"""
# # You are a language evaluator.

# # Compare the following two paragraphs:
# # - Original text (clean and correct)
# # - Voice-generated text (may contain spelling, grammar, or contextual errors)

# # Your task is to detect and list:
# # 1. Words or phrases that are spelled incorrectly.
# # 2. Words or phrases that are substituted or changed.
# # 3. Words or phrases that are missing entirely.
# # 4. Words or phrases that are added in the voice text but not present in the original.

# # Respond in this format:

# # Missing Words: <list>
# # Changed Words: <list of original → voice word>
# # Spelling Errors: <list>
# # Inserted Words: <list>
# # Explanation: <short summary of all issues>

# # Original Text:
# # {original}

# # Voice Text:
# # {generated}
# # """

# #     try:
# #         response = model.generate_content(prompt)
# #         gemini_result = response.text.strip()

# #         final_output = f"{gemini_result}\n\nCalculated WER (Manual): {calculated_wer}%"

# #         return jsonify({"result": final_output})

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # --- START SERVER ---
# # if __name__ == "__main__":
# #     app.run(debug=True) 








# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# from jiwer import wer

# # --- CONFIG ---
# API_KEY = "AIzaSyA-Uw8bI-bT-ceQR-0sN3c6geFceOElKPM"  # Replace this
# MODEL_NAME = "models/gemini-1.5-flash"

# # --- INITIALIZE APP ---
# app = Flask(__name__, template_folder='templates')

# # --- CONFIGURE GEMINI ---
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name=MODEL_NAME)

# # --- HOME PAGE ---
# @app.route("/")
# def index():
#     return render_template("index.html")

# # --- ACCURACY CHECK ROUTE ---
# @app.route("/evaluate", methods=["POST"])
# def evaluate():
#     data = request.json
#     original = data.get("original", "")
#     generated = data.get("generated", "")

#     # Calculate Word Error Rate (WER)
#     calculated_wer = round(wer(original, generated) * 100, 2)

#     prompt = f"""
# You are a language evaluator.

# Compare the following two paragraphs:
# 1. Original Text (clean and correct)
# 2. Voice Text (possibly with errors)

# Tasks:
# - Give an estimated Accuracy percentage (0–100%) comparing both texts.
# - List:
#    - Spelling errors
#    - Changed words/phrases (original → voice)
#    - Missing words/phrases
#    - Extra/inserted words
# - Then write a brief explanation of all issues.

# Respond in this format:

# Accuracy: <value>%
# Spelling Errors: <list>
# Changed Words: <list>
# Missing Words: <list>
# Inserted Words: <list>
# Explanation: <short explanation>

# Original:
# {original}

# Voice:
# {generated}
# """

#     try:
#         response = model.generate_content(prompt)
#         result_text = response.text.strip()

#         # Add WER info
#         result_text += f"\n\nWER (Word Error Rate): {calculated_wer}%"

#         return jsonify({"result": result_text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # --- START SERVER ---
# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# --- CONFIG ---
API_KEY = "AIzaSyA-Uw8bI-bT-ceQR-0sN3c6geFceOElKPM"  # Replace with your actual key
MODEL_NAME = "models/gemini-1.5-flash"

# --- INITIALIZE ---
app = Flask(__name__, template_folder="templates")

# --- SETUP GEMINI ---
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name=MODEL_NAME)

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    question = data.get("original", "")

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
        return jsonify({"error": str(e)}), 500

# --- RUN ---
if __name__ == "__main__":
    app.run(debug=True)

