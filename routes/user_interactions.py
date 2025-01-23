from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from config import db, bcrypt
from models import User, Klasse, Lehrer, Schüler, Anwesenheit, Noten, Schedule
from datetime import datetime

user_interactions = Blueprint("user_interactions", __name__)

@user_interactions.route('/reset_password', methods=["GET", "POST"])
@login_required
def reset_password():

    if request.method == "POST":

        try:
            data = request.json

            if not data:
                return jsonify({"message": "Missing input"}), 400
            
            user_id = session.get("user_id")
            user = User.query.filter_by(id=user_id).first()

            if user:
                user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
                db.session.commit()
                return jsonify({"message": "Passwort wurde erfolgreich geändert! Bitte loggen Sie sich erneut an.",
                                "redirect_url": "/logout"}), 201
            
            return jsonify({"message": "Passwort wurde zurückgesetzt!"}), 200
        
        except SQLAlchemyError:
            db.session.rollback()
            print("An SQLAlchemy error occurred: ", e)
            return jsonify({"message": "Fehler beim Zurücksetzen des Passworts"}), 500
        
        except Exception as e:
            print("Exception in reset_password: ", e)
            return jsonify({"message": "An unexpected error occurred"}), 500

    return render_template("reset_password.html")

@user_interactions.route('/inhalte_einsehen', methods=["GET"])
@login_required
def inhalte_einsehen():

    return render_template("inhalte_einsehen.html")

@user_interactions.route('/kurse_einsehen', methods=["GET"])
@login_required
def kurse_einsehen():

    return render_template("kurse_einsehen.html")

@user_interactions.route('/noten_anwesenheit_einsehen', methods=["GET", "POST"])
@login_required
def noten_anwesenheit_einsehen():

    if request.method == "POST":
    
        try:
                
            noten = Noten.query.filter_by(schüler_id=current_user.id).first()
            anwesenheit = Anwesenheit.query.filter_by(schüler_id=current_user.id).first()

            if not noten and not anwesenheit:
                return jsonify({"message": "Keine Daten vorhanden"}), 401
                
            noten_schüler = {
                "Mathematik": noten.mathematik,
                "Deutsch": noten.deutsch, 
                "Sachunterricht": noten.sachunterricht,
                "Kunst": noten.kunst,
                "Sport": noten.sport,
                "Religion": noten.religion,
                "Englisch": noten.englisch,
                "Musik": noten.musik,
                "Geschichte": noten.geschichte
            }

            anwesenheit_schüler = {
                "Mathematik": anwesenheit.mathematik,
                "Deutsch": anwesenheit.deutsch, 
                "Sachunterricht": anwesenheit.sachunterricht,
                "Kunst": anwesenheit.kunst,
                "Sport": anwesenheit.sport,
                "Religion": anwesenheit.religion,
                "Englisch": anwesenheit.englisch,
                "Musik": anwesenheit.musik,
                "Geschichte": anwesenheit.geschichte
            }

            return jsonify({"noten": noten_schüler,
                            "anwesenheit": anwesenheit_schüler}), 200
            
        except SQLAlchemyError:
            print("An SQLAlchemy error occurred: ", e)
            return jsonify({"message": "Fehler beim Zurücksetzen des Passworts"}), 500
        
        except Exception as e:
            print("Exception in noten_anwesenheit_einsehen: ", e)
            return jsonify({"message": "An unexpected error occurred"}), 500
    
    return render_template("noten_anwesenheit_einsehen.html")

@user_interactions.route('/schedule_student', methods=["GET"])
@login_required
def schedule_student():

    return render_template("schedule_student.html")

@user_interactions.route('/schedule_teacher', methods=["GET"])
@login_required
def schedule_teacher():

    return render_template("schedule_teacher.html")

# Route für den Stundenplan des Lehrers
@user_interactions.route('/teacher/schedule')
@login_required
def teacher_schedule():
    if current_user.role != 'Lehrer':
        return redirect(url_for('authentication.login'))
    
    # Hole alle Stundenplan-Daten des Lehrers
    schedule = Schedule.query.filter_by(lehrer_id=current_user.id).all()

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
@user_interactions.route('/teacher/students')
@login_required
def teacher_students():
    if current_user.role != 'Lehrer':
        return redirect(url_for('authentication.login'))
    
    students = Schüler.query.filter_by(lehrer_id=current_user.id).all()
    return render_template('teacher_students.html', students=students)

# # Route für einzelne Schülerdetails
@user_interactions.route('/teacher/student/<int:id>')
@login_required
def teacher_student_detail(id):
    if current_user.role != 'Lehrer':
        return redirect(url_for('authentication.login'))
    
    student = Schüler.query.get_or_404(id)
    return render_template('teacher_student_detail.html', student=student)

# # Route für Schülerprofil bearbeiten
@user_interactions.route('/teacher/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if current_user.role != 'Lehrer':
        return redirect(url_for('authentication.login'))
    
    student = Schüler.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.class_group = request.form['class_group']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('teacher_students'))
    
    return render_template('edit_student.html', student=student)

# # Route für Schülerprofil löschen
@user_interactions.route('/teacher/student/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    if current_user.role != 'Lehrer':
        return redirect(url_for('authentication.login'))
    
    student = Schüler.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('teacher_students'))

@user_interactions.route('/verwalter/inhalte_verwalten')
@login_required
def inhalte_verwalten():

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    return render_template('inhalte_verwalten.html')

@user_interactions.route('/verwalter/benutzer_verwalten')
@login_required
def benutzer_verwalten():

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    return render_template('benutzer_verwalten.html')


@user_interactions.route('/klassen')
@login_required
def klassen():

    try:

        klassen = None

        if current_user.role == "Verwalter":
            klassen = Klasse.query.all()

        elif current_user.role == "Lehrer":
            klassen = Klasse.query.filter_by(lehrer_id=current_user.id)

        
        return render_template("klassen.html", klassen=klassen)
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print("an error occurred in /klassen : ", e)

    except Exception as e:
        print("error in /klassen: ", e)

@user_interactions.route('/klassen/<int:id>')
@login_required
def klassen_info(id):

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    schüler_liste = Klasse.query.filter_by(id=id).with_entities(Klasse.schüler_id, Klasse.schüler_name).all()

    if schüler_liste:
        return render_template('klassen_info.html', schüler_liste=schüler_liste)
    
@user_interactions.route("/schüler/<int:id>")
@login_required
def schüler_info(id):

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    anwesenheiten = Anwesenheit.query.filter_by(schüler_id=id).with_entities(
        Anwesenheit.mathematik, Anwesenheit.deutsch, Anwesenheit.sachunterricht, Anwesenheit.kunst, Anwesenheit.sport,
        Anwesenheit.religion, Anwesenheit.englisch, Anwesenheit.musik, Anwesenheit.geschichte).first()
    noten = Noten.query.filter_by(schüler_id=id).with_entities(
        Noten.mathematik, Noten.deutsch, Noten.sachunterricht, Noten.kunst, Noten.sport, Noten.religion, Noten.englisch,
        Noten.musik, Noten.geschichte).first()
    
    fächer = ["Mathematik", "Deutsch", "Sachunterricht", "Kunst", "Sport", "Relgion", "Englisch", "Musik", "Geschichte"]

    noten_liste = zip(fächer, noten)
    anwesenheiten_liste = zip(fächer, anwesenheiten)
    if anwesenheiten and noten:
        return render_template("schüler_info.html", anwesenheiten_liste=anwesenheiten_liste, noten_liste=noten_liste)
    
@user_interactions.route('/verwalter/inhalte_verwalten/lehrer')
@login_required
def lehrer():

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    schüler_liste = User.query.filter_by(role="Schüler").all()

    if schüler_liste:
        return render_template('')


@user_interactions.route('/verwalter/inhalte_verwalten/stundenplan_verwalten')
@login_required
def stundenplan_verwalten():

    if current_user.role != "Verwalter":
        return redirect(url_for('authentication.login'))
    
    return render_template('inhalte_verwalten.html')