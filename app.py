from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import joblib
import pyodbc
from config import DB_CONFIG

app = Flask(__name__)

# Load the saved model and scaler
model = joblib.load(r"C:\Users\LENOVO\venv\career_predictor\Classifier_model3.pkl")
scaler = joblib.load(r"C:\Users\LENOVO\venv\career_predictor\scaler3.pkl")

# Career labels
career_labels = {
    0: "Software Engineer", 1: "Business Owner", 2: "Unknown", 3: "Banker",
    4: "Lawyer", 5: "Accountant", 6: "Doctor", 7: "Real Estate Developer",
    8: "Stock Investor", 9: "Construction Engineer", 10: "Artist",
    11: "Game Developer", 12: "Government Officer", 13: "Teacher",
    14: "Designer", 15: "Scientist", 16: "Writer"
}

# Database connection
def get_db_connection():
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        "Trusted_connection=yes;"
    )
    return pyodbc.connect(conn_str)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# ----------------- Prediction Page -------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Collect form data
        gender = int(request.form['gender'])
        part_time_job = int(request.form['part_time_job'])
        absence_days = int(request.form['absence_days'])
        extracurricular_activities = int(request.form['extracurricular_activities'])
        self_study_hours = float(request.form['weekly_self_study_hours'])
        math = float(request.form['math_score'])
        history = float(request.form['history_score'])
        physics = float(request.form['physics_score'])
        chemistry = float(request.form['chemistry_score'])
        biology = float(request.form['biology_score'])
        english = float(request.form['english_score'])
        geography = float(request.form['geography_score'])

        # Calculate average score
        average_score = (math + history + physics + chemistry + biology + english + geography) / 7

        # Arrange input in correct order
        input_data = pd.DataFrame([[gender, part_time_job, absence_days, extracurricular_activities,
                                    self_study_hours, math, history, physics, chemistry,
                                    biology, english, geography, average_score]],
                                  columns=['gender', 'part_time_job', 'absence_days', 'extracurricular_activities',
                                           'weekly_self_study_hours', 'math_score', 'history_score',
                                           'physics_score', 'chemistry_score', 'biology_score',
                                           'english_score', 'geography_score', 'average_score'])

        # Scale and predict
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)

        # Map predicted number to career name
        career = career_labels.get(prediction[0], "Unknown Career")

        return render_template('index.html', prediction_text=f"Predicted Career: {career}")

    return render_template('index.html')

# ----------------- Student Data Management -------------------
@app.route('/student_data')
def student_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM student_data')
    students = cursor.fetchall()
    conn.close()
    return render_template('student_data.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    conn = get_db_connection()
    cursor = conn.cursor()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    gender = request.form['gender']
    cursor.execute('INSERT INTO student_data (first_name, last_name, email, gender) VALUES (?, ?, ?, ?)',
                   (first_name, last_name, email, gender))
    conn.commit()
    conn.close()
    return redirect(url_for('student_data'))

@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    gender = request.form['gender']
    cursor.execute('''
        UPDATE student_data
        SET first_name=?, last_name=?, email=?, gender=?
        WHERE student_id=?
    ''', (first_name, last_name, email, gender, student_id))
    conn.commit()
    conn.close()
    return redirect(url_for('student_data'))

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM student_data WHERE student_id=?', (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('student_data'))

# ----------------- Academic Info Management -------------------
@app.route('/academic_info')
def academic_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM academic_info')
    academics = cursor.fetchall()
    conn.close()
    return render_template('academic_info.html', academics=academics)

@app.route('/add_academic', methods=['POST'])
def add_academic():
    conn = get_db_connection()
    cursor = conn.cursor()
    student_id = request.form['student_id']
    absence_days = request.form['absence_days']
    part_time_job = request.form['part_time_job']
    extracurricular_activities = request.form['extracurricular_activities']
    weekly_self_study_hours = request.form['weekly_self_study_hours']
    career_aspiration = request.form['career_aspiration']

    cursor.execute('''
        INSERT INTO academic_info (student_id, absence_days, part_time_job, extracurricular_activities, weekly_self_study_hours, career_aspiration)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, absence_days, part_time_job, extracurricular_activities, weekly_self_study_hours, career_aspiration))
    conn.commit()
    conn.close()
    return redirect(url_for('academic_info'))

@app.route('/update_academic/<int:record_id>', methods=['POST'])
def update_academic(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    absence_days = request.form['absence_days']
    part_time_job = request.form['part_time_job']
    extracurricular_activities = request.form['extracurricular_activities']
    weekly_self_study_hours = request.form['weekly_self_study_hours']
    career_aspiration = request.form['career_aspiration']

    cursor.execute('''
        UPDATE academic_info
        SET absence_days=?, part_time_job=?, extracurricular_activities=?, weekly_self_study_hours=?, career_aspiration=?
        WHERE record_id=?
    ''', (absence_days, part_time_job, extracurricular_activities, weekly_self_study_hours, career_aspiration, record_id))
    conn.commit()
    conn.close()
    return redirect(url_for('academic_info'))

@app.route('/delete_academic/<int:record_id>')
def delete_academic(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM academic_info WHERE record_id=?', (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('academic_info'))

# ----------------- Subjects Management -------------------
@app.route('/subjects')
def subjects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subjects')
    subjects = cursor.fetchall()
    conn.close()
    return render_template('subjects.html', subjects=subjects)

@app.route('/add_subject', methods=['POST'])
def add_subject():
    conn = get_db_connection()
    cursor = conn.cursor()
    student_id = request.form['student_id']
    math_score = request.form['math_score']
    history_score = request.form['history_score']
    physics_score = request.form['physics_score']
    chemistry_score = request.form['chemistry_score']
    biology_score = request.form['biology_score']
    english_score = request.form['english_score']
    geography_score = request.form['geography_score']

    cursor.execute('''
        INSERT INTO subjects (student_id, math_score, history_score, physics_score, chemistry_score,
                              biology_score, english_score, geography_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, math_score, history_score, physics_score, chemistry_score, biology_score, english_score, geography_score))
    conn.commit()
    conn.close()
    return redirect(url_for('subjects'))

@app.route('/update_subject/<int:id>', methods=['POST'])
def update_subject(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    math_score = request.form['math_score']
    history_score = request.form['history_score']
    physics_score = request.form['physics_score']
    chemistry_score = request.form['chemistry_score']
    biology_score = request.form['biology_score']
    english_score = request.form['english_score']
    geography_score = request.form['geography_score']

    cursor.execute('''
        UPDATE subjects
        SET math_score=?, history_score=?, physics_score=?, chemistry_score=?,
            biology_score=?, english_score=?, geography_score=?
        WHERE id=?
    ''', (math_score, history_score, physics_score, chemistry_score, biology_score, english_score, geography_score, id))
    conn.commit()
    conn.close()
    return redirect(url_for('subjects'))

@app.route('/delete_subject/<int:id>')
def delete_subject(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subjects WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('subjects'))

if __name__ == "__main__":
    app.run(debug=True)