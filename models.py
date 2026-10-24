from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Table 1: Staff/Admin Login ke liye
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Password hash hoke save hoga

# Table 2: Student Enquiries ke liye
class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)