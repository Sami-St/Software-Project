from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from config import db, bcrypt
from models import User, Anwesenheit, Noten

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

            user_id = session.get("user_id")

            if user_id:
                
                noten = Noten.query.filter_by(schüler_id=user_id).first()
                anwesenheit = Anwesenheit.query.filter_by(schüler_id=user_id).first()

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
        
            return jsonify({"message": "User existiert nicht"}), 404
            
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