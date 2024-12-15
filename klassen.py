import sqlite3
from datenbank import Database 

class Klassenzimmer:
    def __init__(self):
        self.db = Database()  # Verbindung zur Datenbank
        self.conn = self.db.__connect_to_db()  # Verbindung zur DB herstellen

    def Klasse_hinzufuegen(self, klassen_name):
        """Fügt eine neue Klasse hinzu."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO klassen (klassen_name) VALUES (?)", (klassen_name,))
            self.conn.commit()
            print(f"Die Klasse {klassen_name} wurde hinzugefügt.")
        except Exception as e:
            print(f"Fehler beim Hinzufügen der Klasse: {e}")
        
    def Schueler_hinzufuegen(self, klassen_name, schueler_name):
        """Fügt einen Schüler zu einer Klasse hinzu."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO schueler (klassen_name, schueler_name) VALUES (?, ?)", (klassen_name, schueler_name))
            self.conn.commit()
            print(f"{schueler_name} wurde zur Klasse {klassen_name} hinzugefügt.")
        except Exception as e:
            print(f"Fehler beim Hinzufügen des Schülers: {e}")
        
    def Stundenplan_zuweisen(self, klassen_name, tag, zeit, fach):
        """Weist dem Stundenplan einer Klasse ein Fach zu."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO stundenplan (klassen_name, tag, zeit, fach) VALUES (?, ?, ?, ?)", (klassen_name, tag, zeit, fach))
            self.conn.commit()
            print(f"Stundenplan zu {klassen_name} hinzugefügt: {fach} am {tag} um {zeit}")
        except Exception as e:
            print(f"Fehler beim Zuweisen des Stundenplans: {e}")

    def Klassenzimmer_anzeigen(self):
        """Zeigt die Klassen, Schüler und deren Stundenpläne an."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM klassen")
            klassen = cursor.fetchall()

            for klasse in klassen:
                klassen_name = klasse[0]
                print(f"\nKlasse: {klassen_name}")

                cursor.execute("SELECT schueler_name FROM schueler WHERE klassen_name = ?", (klassen_name,))
                schueler = cursor.fetchall()
                print("  Schüler:")
                for schueler_name in schueler:
                    print(f"    {schueler_name[0]}")

                print("\n  Stundenplan:")
                cursor.execute("SELECT tag, zeit, fach FROM stundenplan WHERE klassen_name = ?", (klassen_name,))
                stundenplan = cursor.fetchall()
                for eintrag in stundenplan:
                    print(f"    {eintrag[1]}: {eintrag[2]} ({eintrag[0]})")
        except Exception as e:
            print(f"Fehler beim Anzeigen des Klassenzimmers: {e}")
