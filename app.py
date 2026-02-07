# app.py - Flask web app for Gurukul Convent School data

from flask import Flask, render_template_string, request, jsonify
from data import school_data  # Import data from data.py

app = Flask(__name__)

# Home page: Displays a summary of the school
@app.route('/')
def home():
    summary = f"""
    <h1>Welcome to {school_data['basic_details']['name']}</h1>
    <p><strong>Type:</strong> {school_data['basic_details']['type']}</p>
    <p><strong>Established:</strong> {school_data['basic_details']['established']}</p>
    <p><strong>Address:</strong> {school_data['address']}</p>
    <p><strong>Vision:</strong> {school_data['vision_mission_motto']['vision']}</p>
    <p><strong>Motto:</strong> {school_data['vision_mission_motto']['motto']}</p>
    <p><strong>GCS AI Project Founders:</strong> {', '.join(school_data['gcs_ai_project']['founders'])}</p>
    <ul>
        <li><a href="/details/basic">Basic Details</a></li>
        <li><a href="/details/staff">Teaching Staff</a></li>
        <li><a href="/details/class11">Class 11 Students</a></li>
        <li><a href="/details/fees">Fee Structure</a></li>
        <li><a href="/search">Search (e.g., student or staff name)</a></li>
    </ul>
    """
    return render_template_string(summary)

# Detailed view for a section
@app.route('/details/<section>')
def details(section):
    if section == 'basic':
        data = school_data['basic_details']
    elif section == 'staff':
        data = school_data['teaching_staff']
    elif section == 'class11':
        data = school_data['class_11']
    elif section == 'fees':
        data = school_data['fee_structure']
    else:
        return "Section not found", 404
    
    html = f"<h1>{section.title()} Details</h1><pre>{data}</pre><a href='/'>Back to Home</a>"
    return render_template_string(html)

# Search endpoint (simple AI-like query for names)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '').lower()
        results = []
        
        # Search in Class 11 students
        for student in school_data['class_11']['boys'] + school_data['class_11']['girls']:
            if query in student.lower():
                results.append(f"Student: {student}")
        
        # Search in staff
        for teacher in school_data['teaching_staff']['senior_teachers'] + school_data['teaching_staff']['junior_teachers']:
            if query in teacher['name'].lower():
                results.append(f"Staff: {teacher['name']} ({teacher.get('subject', 'N/A')})")
        
        if not results:
            results = ["No matches found."]
        
        return render_template_string(f"<h1>Search Results for '{query}'</h1><ul>{''.join(f'<li>{r}</li>' for r in results)}</ul><a href='/'>Back</a>")
    
    # GET: Show search form
    form = """
    <h1>Search School Data</h1>
    <form method="post">
        <input type="text" name="query" placeholder="Enter name (e.g., Shashi Kapoor)">
        <button type="submit">Search</button>
    </form>
    <a href="/">Back to Home</a>
    """
    return render_template_string(form)

# API endpoint for JSON data (useful for AI integrations)
@app.route('/api/data')
def api_data():
    return jsonify(school_data)

if __name__ == '__main__':
    app.run(debug=True)
