from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db=SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(20),default='Trekker') # Admin,Staff,Trekker

    # Relationships
    bookings = db.relationship("Booking",backref="user",lazy=True)
    staff_profile = db.relationship("StaffProfile",backref="user",uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Trek(db.Model):
    __tablename__='treks'
    id=db.Column(db.Integer,primary_key=True)
    trek_name=db.Column(db.String(100),nullable=False)
    difficulty=db.Column(db.String(20),default='Easy') # Easy,Moderate,Hard
    duration=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(20),default='Open') # Open,Closed,Completed 
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey("staff_profiles.id"),nullable=True)

    # Relationships
    bookings = db.relationship("Booking",backref="trek",lazy=True)

    def __repr__(self):
        return f"<Trek {self.trek_name}>"


class StaffProfile(db.Model):
    __tablename__='staff_profiles'
    id=db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True)
    phone=db.Column(db.String(15),nullable=False)
    experience=db.Column(db.Integer)
    status=db.Column(db.String(20),default='not assigned') # assigned,not assigned 

    # Relationships
    treks = db.relationship("Trek",backref="assigned_staff",lazy=True)

    def __repr__(self):
        return f"<StaffProfile User ID {self.id}>"


class Booking(db.Model):
    __tablename__="bookings"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("treks.id"),nullable=False)
    booking_status = db.Column(db.String(20),default="Pending")  # Pending, Approved, Cancelled
    booking_date = db.Column(db.DateTime,default=datetime.utcnow)
    payment_status = db.Column(db.String(20),default="Pending")  # Pending, Paid, Failed

    def __repr__(self):
        return f"<Booking {self.id}>"



