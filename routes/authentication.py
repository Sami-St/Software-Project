from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Fächer, Klasse
from config import db, bcrypt

authentication = Blueprint("authentication", __name__)

@authentication.route('/verwalter/register', methods=["POST", "GET"])
@login_required
def register():

    if request.method == "POST":
    
        if current_user.role != "Verwalter":
            return redirect(url_for("authentication.login"))
        
        data = request.json

        if not data:
            return jsonify({"message": "Missing credentials"}), 400
        
        try:
            new_user = User(
                username= data["username"],
                email = data["email"],
                password= bcrypt.generate_password_hash(data["password"]).decode('utf-8'),
                role= data["user-type"]
            )

            fächer = data["fächer"]
            klasse = data["klasse"]

            email_exists = User.query.filter_by(email=new_user.email).first() 
            klasse_exists = Klasse.query.filter_by(name=klasse)

            if email_exists:
                return jsonify({"message": "Email Adresse existiert bereits."}), 409
            
            db.session.add(new_user)
            db.session.flush() # Flush to get the new_user ID without committing
            
            if klasse:
                
                if klasse_exists:

                    klasse_exists.schüler_id=new_user.id
                    klasse_exists.scüler_name=new_user.username

                else:

                    new_klasse = Klasse(schüler_id=new_user.id, schüler_name=new_user.username, name=klasse)
                    db.session.add(new_klasse)

            if fächer:

                for fach_name in fächer:
                    fach = Fächer(fach_name=fach_name, lehrer_id=new_user.id)
                    db.session.add(fach)
                
            db.session.commit()
                
            return jsonify({"message": "Registierung abgeschlossen! Sie werden in Kürze weitergeleitet."}), 201
          
        except SQLAlchemyError as e:
            db.session.rollback()
            print("An SQLAlchemy error occurred: ", e)
            return jsonify({"message": "Server error, could not create user"}), 500
        
        except Exception as e:
            print("An error occured: ", e)
            return jsonify({"message": "An unexpected error occurred"}), 500

    return render_template("register.html")

@authentication.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        try:
            data = request.json

            if not data:
                return jsonify({"message": "Missing input"}), 400
                

            user = User.query.filter_by(email=data["email"]).first()

            if user and bcrypt.check_password_hash(user.password, data["password"]):
                login_user(user)
                session['user_role'] = user.role
                session['user_id'] = user.id

                return jsonify({"message": "Success!",
                                "redirect_url": "/dashboard"}), 200

            else:
                return jsonify({"message": "Email oder Passwort ist falsch"}), 401
        
        except Exception as e:
            print("An exception occurred in login route: ", e)
            return jsonify({"message": "Internal server error"}), 500
        
    return render_template("login.html")

@authentication.route("/get_user", methods=["POST"])
@login_required
def get_user():

    try:
        user_id = session.get("user_id")
        user = User.query.filter_by(id=user_id).with_entities(User.email, User.role).first()
        user_info = {
            "user_id": user_id,
            "email": user.email,
            "role": user.role
        }

        if user_id and user:
            return jsonify({"user": user_info}), 200
        
        return jsonify({"message": "Failed to fetch user data"}), 401
    
    except Exception as e:
        print("Exception occurred in /get_user: ", str(e))
        return jsonify({"message": "An unexpteced error occurred"}), 500

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('authentication.login'))

# @authentication.route("/testlogin", methods=["GET", "POST"])
    