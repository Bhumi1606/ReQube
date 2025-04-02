import json
import requests  # For making API calls
import os  # For environment variables

# ✅ Define priority rules
PRIORITY_RULES = {
    "Must Have": ["upload", "store", "manage", "validate", "version control"],
    "Should Have": ["real-time", "clarification", "track", "approval"],
    "Could Have": ["generate", "export", "download"],
    "Won't Have": ["optional", "future", "later"]
}

# ✅ Function to assign priority based on keywords
def assign_priority(description):
    description = description.lower()
    for priority, keywords in PRIORITY_RULES.items():
        if any(keyword in description for keyword in keywords):
            return priority
    return None  # Return None so that Gemini API can handle it later

# ✅ Function to categorize functional vs non-functional requirements
def categorize_requirements(description):
    functional_keywords = ["upload", "manage", "validate", "store"]
    non_functional_keywords = ["real-time", "performance", "scalability", "security"]
    
    description_lower = description.lower()
    
    if any(keyword in description_lower for keyword in functional_keywords):
        return "Functional"
    elif any(keyword in description_lower for keyword in non_functional_keywords):
        return "Non-Functional"
    else:
        return "Uncategorized"

# ✅ Function to get AI-based prioritization from Gemini
def get_priority_from_gemini(requirements_list):
    API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    API_KEY = os.getenv("GEMINI_API_KEY")  # Use environment variable

    if not API_KEY:
        print("❌ Error: Gemini API key not found! Set GEMINI_API_KEY in environment variables.")
        return []

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = (
        "You are an experienced Project Manager. Analyze the following software requirements "
        "and prioritize them using the MOSCOW method (Must Have, Should Have, Could Have, Won't Have). "
        "Ensure core functionalities are 'Must Have', important but non-critical features are 'Should Have', "
        "useful features are 'Could Have', and non-essential ones are 'Won't Have'. "
        "Provide the updated priorities in JSON format as a dictionary with requirement ID as key "
        "and priority as value."
    )

    # Prepare the input for Gemini API
    input_text = "\n".join([f"{req['ID']}: {req['Requirement']}" for req in requirements_list])

    payload = {
        "contents": [{"parts": [{"text": prompt + "\n\n" + input_text}]}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raises HTTP errors if any
        response_data = response.json()
        
        # Extract the prioritized data from API response
        gemini_priorities = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
        return json.loads(gemini_priorities)  # Convert API text response into dictionary

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return {}

# ✅ Function to convert prioritized requirements into text format
def convert_to_text_format(data):
    text_output = "Prioritized Requirements:\n\n"
    text_output += "Functional Requirements:\n"
    for req in data.get("requirements", []):
        if req.get("category") == "Functional":
            text_output += f"Requirement ID: {req.get('ID', 'N/A')}\n"
            text_output += f"Description: {req.get('Requirement', 'N/A')}\n"
            text_output += f"Priority: {req.get('priority', 'N/A')}\n"
            text_output += "-" * 50 + "\n"
    
    text_output += "\nNon-Functional Requirements:\n"
    for req in data.get("requirements", []):
        if req.get("category") == "Non-Functional":
            text_output += f"Requirement ID: {req.get('ID', 'N/A')}\n"
            text_output += f"Description: {req.get('Requirement', 'N/A')}\n"
            text_output += f"Priority: {req.get('priority', 'N/A')}\n"
            text_output += "-" * 50 + "\n"
    
    return text_output

# ✅ Main function to process JSON
def prioritize_requirements(input_file="output.json", output_file="prioritized_requirements.txt"):
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in {input_file}.")
        return

    unmatched_requirements = []  # Store requirements that need AI prioritization

    for req in data.get("requirements", []):
        if "Requirement" not in req or "ID" not in req:
            print(f"⚠️ Warning: Requirement missing expected fields {req}")
            continue

        priority = assign_priority(req["Requirement"])
        if priority:
            req["priority"] = priority
        else:
            unmatched_requirements.append(req)  # Send these to Gemini API for prioritization
        
        req["category"] = categorize_requirements(req["Requirement"])  # Categorize as functional or non-functional

    # If AI prioritization is needed
    if unmatched_requirements:
        print("🔍 Sending unmatched requirements to Gemini API for prioritization...")
        corrected_priorities = get_priority_from_gemini(unmatched_requirements)

        for req in unmatched_requirements:
            req_id = req["ID"]
            if req_id in corrected_priorities:
                req["priority"] = corrected_priorities[req_id]
            else:
                req["priority"] = "Uncategorized"  # Default if Gemini API fails

    # Convert the prioritized data to a human-readable text format
    text_output = convert_to_text_format(data)

    # Save the text output to a .txt file
    with open(output_file, "w") as file:
        file.write(text_output)

    print(f"✅ Prioritized requirements saved to {output_file}")

# ✅ Run prioritization
if __name__ == "__main__":
    prioritize_requirements()

# import json
# import requests  # For making API calls
# import os  # For environment variables
# from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # ✅ Define priority rules
# PRIORITY_RULES = {
#     "Must Have": ["upload", "store", "manage", "validate", "version control"],
#     "Should Have": ["real-time", "clarification", "track", "approval"],
#     "Could Have": ["generate", "export", "download"],
#     "Won't Have": ["optional", "future", "later"]
# }

# def assign_priority(description):
#     description = description.lower()
#     for priority, keywords in PRIORITY_RULES.items():
#         if any(keyword in description for keyword in keywords):
#             return priority
#     return "Uncategorized"

# def categorize_requirements(description):
#     functional_keywords = ["upload", "manage", "validate", "store"]
#     non_functional_keywords = ["real-time", "performance", "scalability", "security"]
#     description_lower = description.lower()
#     if any(keyword in description_lower for keyword in functional_keywords):
#         return "Functional"
#     elif any(keyword in description_lower for keyword in non_functional_keywords):
#         return "Non-Functional"
#     else:
#         return "Uncategorized"

# def prioritize_requirements(input_data):
#     for req in input_data.get("requirements", []):
#         req["priority"] = assign_priority(req["Requirement"])
#         req["category"] = categorize_requirements(req["Requirement"])
#     return input_data

# def get_prioritized_requirements(input_file):
#     try:
#         with open(input_file, "r") as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         return {"error": "File not found."}
#     except json.JSONDecodeError:
#         return {"error": "Invalid JSON format."}
#     return prioritize_requirements(data)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             prioritized_data = get_prioritized_requirements(filepath)
#             return render_template("result1.html", result=prioritized_data)  # Redirecting to result1.html
#     return render_template("index.html")



# if __name__ == '__main__':
#     app.run(debug=True)

# import json
# import os  # For environment variables and file handling
# from flask import Flask, render_template, request, redirect, url_for, session
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# # Set a secret key for session management
# app.secret_key = 'your_secret_key_here'

# # Upload folder for storing uploaded files
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Define priority rules
# PRIORITY_RULES = {
#     "Must Have": ["upload", "store", "manage", "validate", "version control"],
#     "Should Have": ["real-time", "clarification", "track", "approval"],
#     "Could Have": ["generate", "export", "download"],
#     "Won't Have": ["optional", "future", "later"]
# }

# # Function to assign priority based on keywords
# def assign_priority(description):
#     description = description.lower()
#     for priority, keywords in PRIORITY_RULES.items():
#         if any(keyword in description for keyword in keywords):
#             return priority
#     return "Uncategorized"

# # Function to categorize functional vs non-functional requirements
# def categorize_requirements(description):
#     functional_keywords = ["upload", "manage", "validate", "store"]
#     non_functional_keywords = ["real-time", "performance", "scalability", "security"]
#     description_lower = description.lower()

#     if any(keyword in description_lower for keyword in functional_keywords):
#         return "Functional"
#     elif any(keyword in description_lower for keyword in non_functional_keywords):
#         return "Non-Functional"
#     else:
#         return "Uncategorized"

# # Function to prioritize requirements
# def prioritize_requirements(input_data):
#     for req in input_data.get("requirements", []):
#         req["priority"] = assign_priority(req["Requirement"])
#         req["category"] = categorize_requirements(req["Requirement"])
#     return input_data

# # Function to read and prioritize JSON file
# def get_prioritized_requirements(input_file):
#     try:
#         with open(input_file, "r") as file:
#             data = json.load(file)
#             return prioritize_requirements(data)
#     except FileNotFoundError:
#         return {"error": "File not found."}
#     except json.JSONDecodeError:
#         return {"error": "Invalid JSON format."}

# # Flask Routes
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         if file and file.filename.endswith('.json'):  # Ensure valid JSON file
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             # Save the file path in session for later use
#             session['uploaded_file'] = filepath

#             # Process and prioritize the requirements from the uploaded JSON file
#             prioritized_data = get_prioritized_requirements(filepath)
#             return render_template("result1.html", result=prioritized_data)  # Redirect to results page
#         return "Invalid file format. Please upload a valid JSON file."
    
#     return render_template("index.html")

# @app.route('/prioritize', methods=['POST'])
# def prioritize():
#     uploaded_file = session.get('uploaded_file')
#     if uploaded_file:
#         # Process the file (e.g., prioritize requirements)
#         prioritized_data = get_prioritized_requirements(uploaded_file)
#         return render_template("result1.html", result=prioritized_data)
#     return redirect(url_for('index'))  # Redirect back to home if no file is found

# if __name__ == '__main__':
#     app.run(debug=True)
# import json
# import os  # For environment variables and file handling
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# # Set a secret key for session management
# app.secret_key = 'your_secret_key_here'

# # Upload folder for storing uploaded files
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Define priority rules
# PRIORITY_RULES = {
#     "Must Have": ["upload", "store", "manage", "validate", "version control"],
#     "Should Have": ["real-time", "clarification", "track", "approval"],
#     "Could Have": ["generate", "export", "download"],
#     "Won't Have": ["optional", "future", "later"]
# }

# # Function to assign priority based on keywords
# def assign_priority(description):
#     description = description.lower()
#     for priority, keywords in PRIORITY_RULES.items():
#         if any(keyword in description for keyword in keywords):
#             return priority
#     return "Uncategorized"

# # Function to categorize functional vs non-functional requirements
# def categorize_requirements(description):
#     functional_keywords = ["upload", "manage", "validate", "store"]
#     non_functional_keywords = ["real-time", "performance", "scalability", "security"]
#     description_lower = description.lower()

#     if any(keyword in description_lower for keyword in functional_keywords):
#         return "Functional"
#     elif any(keyword in description_lower for keyword in non_functional_keywords):
#         return "Non-Functional"
#     else:
#         return "Uncategorized"

# # Function to prioritize requirements
# def prioritize_requirements(input_data):
#     for req in input_data.get("requirements", []):
#         req["priority"] = assign_priority(req["Requirement"])
#         req["category"] = categorize_requirements(req["Requirement"])
#     return input_data

# # Function to read and prioritize JSON file
# def get_prioritized_requirements(input_file):
#     try:
#         with open(input_file, "r") as file:
#             data = json.load(file)
#             return prioritize_requirements(data)
#     except FileNotFoundError:
#         return {"error": "File not found."}
#     except json.JSONDecodeError:
#         return {"error": "Invalid JSON format."}

# # Flask Routes
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         if file and file.filename.endswith('.json'):  # Ensure valid JSON file
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             # Save the file path in session for later use
#             session['uploaded_file'] = filepath

#             # Process and prioritize the requirements from the uploaded JSON file
#             prioritized_data = get_prioritized_requirements(filepath)
#             if "error" in prioritized_data:
#                 flash(f"❌ {prioritized_data['error']}")
#                 return redirect(url_for('index'))
#             return render_template("result1.html", result=prioritized_data)  # Redirect to results page
#         flash("❌ Invalid file format. Please upload a valid JSON file.")
#         return redirect(url_for('index'))
    
#     return render_template("index.html")

# @app.route('/prioritize', methods=['POST'])
# def prioritize():
#     uploaded_file = session.get('uploaded_file')
#     if uploaded_file:
#         # Process the file (e.g., prioritize requirements)
#         prioritized_data = get_prioritized_requirements(uploaded_file)
#         if "error" in prioritized_data:
#             flash(f"❌ {prioritized_data['error']}")
#             return redirect(url_for('index'))
#         return render_template("result1.html", result=prioritized_data)
#     flash("❌ No file uploaded. Please upload a valid JSON file.")
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
