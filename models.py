from config import db
from flask_login import UserMixin
from sqlalchemy import event

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Lehrer(db.Model):

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    
    user = db.relationship("User", backref="lehrer")
    
class Schüler(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    lehrer_id = db.Column(db.Integer, db.ForeignKey("lehrer.id"))
    
    user = db.relationship("User", backref="schüler")
    lehrer = db.relationship("Lehrer", backref="schüler")


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

class Klasse(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    schüler_id = db.Column(db.Integer, db.ForeignKey("schüler.id"), unique=True)
    schüler_name = db.Column(db.String(30), nullable=False)
    lehrer_id = db.Column(db.Integer, db.ForeignKey("lehrer.id"))
    name = db.Column(db.String(30), nullable=False)

    schüler = db.relationship("Schüler", backref="klasse")
    lehrer = db.relationship("Lehrer", backref="klassen")

class Fächer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fach_name = db.Column(db.String(30), nullable=False)
    lehrer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User", backref="fächer")

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lehrer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(50))
    class_group = db.Column(db.String(50))
    day_of_week = db.Column(db.String(10))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    user = db.relationship("User", backref="schedule")

# populate primary key in the corresponding table based on user role
@event.listens_for(User, "after_insert")
def create_related_records(mapper, connection, target):
    # Check the role and create the corresponding record
    if target.role == "Lehrer":
        connection.execute(
            Lehrer.__table__.insert().values(id=target.id)
        )
    elif target.role == "Schüler":
        # Automatically create a Schüler entry
        connection.execute(
            Schüler.__table__.insert().values(id=target.id)
        )