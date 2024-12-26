from flask import jsonify
from datenbank.database import Database
from models import User
import jwt
import datetime


db = Database()
secret_key = "3b1c60e954f646299c20e9c6b09a0b7d"

def create_token(given_email):

    try:
    
        data = db.get_user_data(given_email)

        if not data:
            raise Exception

        user = User(
            userID = data["userID"],
            email = data["email"],
            rolle = data["rolle"]
        )

        fächer = db.get_fächer(user.userID)

        if not fächer:

            raise Exception

        if user:

            payload = {
                'sub': str(user.userID), 
                'email': user.email,
                'rolle': user.rolle,
                'isAdmin': False,
                "token_type": "access",
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            }
            print("TOKEN PAYLOAD IS: ", payload)

            # für User vom Typ "Lehrer" weitere Claims hinzufügen
            if user.rolle == "Lehrer":
                payload['fächer'] = fächer
                payload['isAdmin'] = True

            token = jwt.encode(payload, secret_key, algorithm="HS256", sort_headers=False)

            return token
        
    except Exception as e:
        print("an exception occurred while creating token: ", e)
        return jsonify({"error": "User ID could not be found."}), 401