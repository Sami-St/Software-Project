import sqlite3
from models import User
from utils import password_utils
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

            hashed_pw = password_utils.hash_pw(user.password)

            self.cursor.execute("""INSERT INTO users (name, email, password, rolle)
                                VALUES (?, ?, ?, ?)""", (user.name, user.email, hashed_pw, user.rolle))
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
    
    def verify_email(self, data):

        try:
            self.conn = self.__connect_to_db()
            self.cursor = self.conn.cursor()
            
            self.cursor.execute("SELECT email FROM users WHERE email = ?", (data, ))
            found_email = self.cursor.fetchone()

            if found_email:
                return True

            return False
        
        except Exception as e:

            print("An exception occurred: ", e)
            return False
        
        finally:

            self.conn.close()
    
    def verify_password(self, email, password):

        try:
            self.conn = self.__connect_to_db()
            self.cursor = self.conn.cursor()
            
            self.cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            results = self.cursor.fetchone()

            pw_exists = password_utils.check_pw(stored_password=results[0], given_password=password)

            if pw_exists:
                return True

            print("verify pw returned none")
            return False
        
        except Exception as e:

            print("An exception occurred: ", e)
            return False
        
        finally:

            self.conn.close()

    def get_user_data(self, email):

        try:

            self.conn = self.__connect_to_db()
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT userID, email, rolle FROM users WHERE email = ?", (email,))
            results = self.cursor.fetchall()

            if not results:
                print("no data found")
                return False
            
            # results ist ein tuple in einer Liste
            user_data = {
                "userID": results[0][0],
                "email": results[0][1],
                "rolle": results[0][2]
            }

            return user_data
        
        except Exception as e:
            print("an exception occurred in func get_user_data, ", e)
            return False
        
    def get_fächer(self, userID):

        
        try:

            liste_fächer = []

            self.conn = self.__connect_to_db()
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT fachName FROM fächer WHERE lehrerID = ?", (userID,))
            results = self.cursor.fetchall()
            
            for tuple in results:
                for fach in tuple:
                    liste_fächer.append(fach)

            if not results:
                print("No fächer found")
                return False
            
            return liste_fächer

        except Exception as e:
            print("An exception occurred in func get_fächer ", e)
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
