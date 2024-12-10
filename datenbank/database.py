import sqlite3
from models import User
from password_utils import hash_password
import os

class Database():

    def __init__(self):
        self.conn = None

    def __connect_to_db(self):

        try:

            db_file_path = 'database/datenbank.db'
            self.conn = sqlite3.connect(os.path.abspath(db_file_path))
            return self.conn
        
        except Exception as e:
            print("Failed to connect to database: ", e)
            return False
        
    # async damit man "await" auf die Funktion anwenden kann in der app.py Datei
    async def create_user(self, user: User):

        self.conn = self.__connect_to_db()
        self.cursor = self.conn.cursor()

        try:

            hashed_pw = hash_password(user.password)

            self.cursor.execute("""INSERT INTO users (name, email, password, rolle)
                                VALUES (?, ?, ?, ?)""", (user.name, user.email, hashed_pw, user.userType))
            self.conn.commit()
            self.cursor.execute("SELECT userID FROM users WHERE email = ?", (user.email, ))
            results = self.cursor.fetchone()

            if not results:
                print("No user id found")
                return None
            
            user_id = results[0]
            print("Succesfully added data!")
            return user_id

        except Exception as e:
            print("An error has occurred while trying to insert data into the database: ", e)
            return False
        
        finally:

            self.conn.close()

    def add_subjects(self, user_id, fächer):

        try:
            self.conn = self.__connect_to_db()
            self.cursor = self.conn.cursor()

            for fach in fächer:
                self.cursor.execute("INSERT INTO fächer (fachName, lehrerID) VALUES (?, ?)", (fach, user_id))
            self.conn.commit()

            return True
        
        except Exception as e:

            print("An exception occured in func add_subjects: ", e)
            return False
        
        finally:

            self.conn.close()

    def del_data(self):

        self.conn = self.__connect_to_db()
        self.cursor = self.conn.cursor()

        self.cursor.execute("DELETE FROM users;")
        self.conn.commit()
        self.cursor.execute("DELETE FROM sqlite_sequence;")
        self.conn.commit()
        self.cursor.execute("DELETE FROM fächer")
        self.conn.commit()

        print("Success delete from all tables!")

        self.conn.close()