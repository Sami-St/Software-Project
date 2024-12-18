from flask import Blueprint, render_template, request, jsonify
from models import User
from datenbank.database import Database

authentication = Blueprint("authentication", __name__)
db = Database()

@authentication.route('/register', methods=["POST", "GET"])
async def register():

    if request.method == "POST":
    
        data = request.json

        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        try:
            user = User(
                name= data["name"],
                email = data["email"],
                password= data["password"],
                userType= data["user-type"]
            )
            fächer = data["fächer"]

            email_exists = db.verify_email(user.email) 

            if email_exists:
                return jsonify({"message": "Email Adresse existiert bereits."}), 409
            
            # db.create_user returns the user ID, which is used to associate subjects (Fächer) with the created user.
            created_user = await db.create_user(user)

            if not created_user:
                return jsonify({"message": "Server error"}), 500
                
            elif created_user and fächer != None:
                
                added_subjects = db.add_subjects(created_user, tuple(fächer))

                if not added_subjects:
                    return jsonify({"message": "Fächer konnten nicht hinzugefügt werden."}), 500

                elif created_user and added_subjects:
                    return jsonify({"message": "Registierung abgeschlossen! Sie werden in Kürze weitergeleitet."}), 201
        
            return jsonify({"message": "Registierung abgeschlossen! Sie werden in Kürze weitergeleitet."}), 201
          
        except Exception as e:
            print("An exception has occured: ", e)
            return jsonify({"message":"An exception occurred"}), 400

    return render_template("register.html")

@authentication.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        data = request.json

        if not data:
            return jsonify({"message": "No data provided"}), 400

        try:
        
            user = User(
                email = data["email"],
                password = data["password"]
            )

            email_valid = db.verify_email(user.email)
            password_valid =  db.verify_password(user.email, user.password)

            if not email_valid or not password_valid:

                return jsonify({"message": "Email oder Passwort ist falsch."}), 401
            
            return jsonify({"message": "Login erfolgreich."}), 201
        
        except Exception as e:
            return jsonify({"message": "Server error"}), 500
        
    return render_template("login.html")