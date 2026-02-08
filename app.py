# app.py
from flask import Flask, render_template, request, jsonify
from data import school_data

app = Flask(__name__)

# Fallback message
FALLBACK = f"Sorry, I don't have information about that. You can contact the school at {', '.join(school_data['gcs_ai']['contact_numbers'])}."

# Keywords mapping
keywords = {
    "school info": "basic_info",
    "timing": "timings",
    "address": "address",
    "management": "management",
    "director": "management",
    "principal": "management",
    "vision": "vision_mission_motto",
    "mission": "vision_mission_motto",
    "motto": "vision_mission_motto",
    "teachers": "senior_teachers",
    "junior teachers": "junior_teachers",
    "staff": "support_staff",
    "fee": "fee_structure",
    "class 11": "class_11_details",
    "infrastructure": "infrastructure",
    "transport": "transport",
    "admission": "admission_requirements",
    "houses": "house_system",
    "house system": "house_system",
    "sports": "sports_activities",
    "activities": "sports_activities",
    "contact": "gcs_ai"
}

def fetch_answer(user_input):
    user_input = user_input.lower()
    for key, value in keywords.items():
        if key in user_input:
            info = school_data.get(value)
            if isinstance(info, dict):
                return "\n".join([f"{k}: {v}" for k, v in info.items()])
            elif isinstance(info, list):
                return ", ".join(info)
            else:
                return str(info)
    return FALLBACK

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("message")
    answer = fetch_answer(user_input)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
