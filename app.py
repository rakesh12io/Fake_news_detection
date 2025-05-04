from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import re
import string
import csv
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something secure

# Files
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
feedback_file = 'feedback.csv'
users_file = 'users.json'

# Clean news text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = clean_text(data['text'])
    vectorized = vectorizer.transform([text])
    prediction = model.predict(vectorized)[0]
    return jsonify({'prediction': 'Real' if prediction == 1 else 'Fake'})

# Submit feedback
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    feedback = data.get('feedback', '')

    if feedback.strip():
        with open(feedback_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, feedback])
        return jsonify({'message': '✅ Thank you for your feedback!'})
    else:
        return jsonify({'message': '⚠️ Feedback cannot be empty.'})

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        users = {}
        if os.path.exists(users_file):
            with open(users_file) as f:
                users = json.load(f)

        if username in users:
            return "User already exists."

        users[username] = password
        with open(users_file, 'w') as f:
            json.dump(users, f)

        return redirect('/login')

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if os.path.exists(users_file):
            with open(users_file) as f:
                users = json.load(f)

            stored_hash = users.get(username)
            if stored_hash and check_password_hash(stored_hash, password):
                session['admin'] = username
                return redirect('/admin')
            else:
                error = "Invalid username or password"
        else:
            error = "No users registered."

    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# Admin route
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    feedbacks = []
    if os.path.exists(feedback_file):
        with open(feedback_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            feedbacks = list(reader)
    return render_template('admin.html', feedbacks=list(enumerate(feedbacks)))

@app.route('/delete-feedback', methods=['POST'])
def delete_feedback():
    if 'admin' not in session:
        return redirect('/login')

    try:
        index_to_delete = int(request.form['index'])
    except (ValueError, TypeError, KeyError):
        return "Invalid index.", 400

    rows = []
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r', encoding='utf-8') as f:
            rows = list(csv.reader(f))

        if 0 <= index_to_delete < len(rows):
            rows.pop(index_to_delete)
            with open(feedback_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)

    return redirect('/admin')

# Download feedback file
@app.route('/download-feedback')
def download_feedback():
    if 'admin' not in session:
        return redirect('/login')

    if os.path.exists(feedback_file):
        return send_file(feedback_file, as_attachment=True)
    return "No feedback available.", 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
