# 📰 Fake News Detection Web App

This is a Flask web application that uses a machine learning model to detect whether a news article is real or fake. It includes user authentication, feedback submission, and an admin dashboard for managing feedback.

## 🚀 Features

- Predict whether news is **Fake** or **Real** using a trained ML model.
- Clean and preprocess user-submitted text.
- Collect user feedback on predictions.
- User signup and login system.
- Admin panel to review and delete feedback.
- Download feedback as a CSV file.

## 🧠 Machine Learning

- The app loads a pre-trained model (`model.pkl`) and vectorizer (`vectorizer.pkl`) using `joblib`.
- News text is cleaned using regex and then vectorized for prediction.

## 🛠 Technologies Used

- Python, Flask
- scikit-learn (for ML model)
- HTML templates (Jinja2)
- CSV & JSON (for feedback and user storage)
- `joblib`, `werkzeug.security`, `re`, `string`

## 📁 Project Structure

project/
│
├── templates/
│ ├── index.html
│ ├── signup.html
│ ├── login.html
│ └── admin.html
│
├── model.pkl
├── vectorizer.pkl
├── feedback.csv
├── users.json
└── app.py




## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/fake-news-detection-app.git
   cd fake-news-detection-app

## Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies:
pip install flask joblib scikit-learn

## Ensure these files are in the root directory:

model.pkl
vectorizer.pkl


## Run the app:
python app.py


