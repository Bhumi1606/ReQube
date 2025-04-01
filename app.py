from flask import Flask, request, render_template, session, redirect, url_for, flash
import requests
import os
from input import extract_text
from werkzeug.utils import secure_filename
import json
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)  
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

def extract_json_from_text(text):
    """Extract valid JSON from a mixed response."""
    match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return {"error": "Extracted text is not valid JSON."}
    return {"error": "No valid JSON found in response."}

def analyze_business_text(input_text):
    """Send text to Gemini API for requirement analysis."""
    if not input_text.strip():
        return {"error": "No valid text provided for analysis."}

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{
            "parts": [{
                "text": f"""
You are a highly skilled Business Analyst with expertise in requirement engineering and documentation. Your task is to analyze structured and unstructured data extracted from various sources, such as PDFs, images, and Excel files. You must:

1. Extract Key Points: Identify and extract the most important details from the given text.
2. Summarize Text: Generate a concise and accurate summary of the extracted content.
3. Classify Requirements: Categorize the extracted information into:
   - Functional Requirements (FRs): Features and behaviors the system must have.
   - Non-Functional Requirements (NFRs): Performance, security, usability, and other constraints.
4. Pose Questions for Missing Information: Identify gaps in the given data and generate precise, well-structured questions to clarify missing or ambiguous details.

### Input Format:
The input will be raw text extracted from a PDF, image, or Excel file, containing business requirements, project details, and user expectations.

### Output Format:
Output only valid JSON inside triple backticks (json ... ).
No additional text or comments.
json
{{
    "key_points": [
        "Summarized key point 1",
        "Summarized key point 2"
    ],
    "summary": "A concise summary of the text.",
    "requirements": {{
        "functional": [
            "FR1: Functional requirement description",
            "FR2: Functional requirement description"
        ],
        "non_functional": [
            "NFR1: Non-functional requirement description",
            "NFR2: Non-functional requirement description"
        ]
    }},
    "missing_info_questions": [
        "Question 1 to clarify missing information",
        "Question 2 to clarify missing information"
    ]
}}

Now, analyze the following text:

{input_text}
"""
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        # Extract response content safely
        result_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")

        # Extract JSON from response
        return extract_json_from_text(result_text)

    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def home():
    session.setdefault("analysis_result", None)

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        input_text = request.form.get("input_text", "").strip()

        extracted_text = ""

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(file_path)

            extracted_text = extract_text(file_path)  

            if not extracted_text:
                flash("Error extracting text from file. Please check the document format.")
                return redirect(url_for("home"))

        final_text = extracted_text if extracted_text else input_text

        if not final_text:
            flash("No valid text provided for analysis.")
            return redirect(url_for("home"))

        analysis_result = analyze_business_text(final_text)
        
        if "error" in analysis_result:
            flash(f"Failed to analyze text: {analysis_result['error']}")
            return redirect(url_for("home"))

        session["analysis_result"] = analysis_result
        session.modified = True
        return redirect(url_for("result"))

    return render_template("index.html", analysis_result=session.get("analysis_result"))

@app.route("/result")
def result():
    analysis_result = session.get("analysis_result")
    if not analysis_result:
        flash("No analysis result found. Please upload a document or enter text first.")
        return redirect(url_for("home"))

    return render_template("result.html", result=analysis_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
