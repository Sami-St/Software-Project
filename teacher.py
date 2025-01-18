from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .routes import app, db
from models import Schedule, Student, Teacher
from datetime import datetime

# Route für den Stundenplan des Lehrers
@app.route('/teacher/schedule')
@login_required
def teacher_schedule():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    # Hole alle Stundenplan-Daten des Lehrers
    schedule = Schedule.query.filter_by(teacher_id=current_user.id).all()

    # Daten nach Wochentagen und Uhrzeiten gruppieren
    timetable = {
        "Montag": [],
        "Dienstag": [],
        "Mittwoch": [],
        "Donnerstag": [],
        "Freitag": []
    }

    for entry in schedule:
        timetable[entry.day_of_week].append(entry)

    return render_template('schedule_teacher.html', timetable=timetable)

# Route für Schülerliste anzeigen
@app.route('/teacher/students')
@login_required
def teacher_students():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    students = Student.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher_students.html', students=students)

# Route für einzelne Schülerdetails
@app.route('/teacher/student/<int:id>')
@login_required
def teacher_student_detail(id):
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(id)
    return render_template('teacher_student_detail.html', student=student)

# Route für Schülerprofil bearbeiten
@app.route('/teacher/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.class_group = request.form['class_group']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('teacher_students'))
    
    return render_template('edit_student.html', student=student)

# Route für Schülerprofil löschen
@app.route('/teacher/student/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('teacher_students'))
