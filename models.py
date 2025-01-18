from config import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Noten(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    schüler_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    schüler_name = db.Column(db.String(30), db.ForeignKey("user.username"), nullable=False)
    mathematik = db.Column(db.Integer, nullable=False)
    deutsch = db.Column(db.Integer, nullable=False)
    sachunterricht = db.Column(db.Integer, nullable=False)
    kunst = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.Integer, nullable=False)
    englisch = db.Column(db.Integer, nullable=False)
    musik = db.Column(db.Integer, nullable=False)
    geschichte = db.Column(db.Integer, nullable=False)

class Anwesenheit(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    schüler_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    schüler_name = db.Column(db.String(30), db.ForeignKey("user.username"), nullable=False)
    mathematik = db.Column(db.Integer, nullable=False)
    deutsch = db.Column(db.Integer, nullable=False)
    sachunterricht = db.Column(db.Integer, nullable=False)
    kunst = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.Integer, nullable=False)
    englisch = db.Column(db.Integer, nullable=False)
    musik = db.Column(db.Integer, nullable=False)
    geschichte = db.Column(db.Integer, nullable=False)

class Klassen(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    schüler_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Fächer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fach_name = db.Column(db.String(30), nullable=False)
    lehrer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    subject = db.Column(db.String(50))
    class_group = db.Column(db.String(50))
    day_of_week = db.Column(db.String(10))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

