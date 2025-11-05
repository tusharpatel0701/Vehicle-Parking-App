from .database import db  # if . is removed then it will try to search for database in root folder so . is placed so that it can check for this file inn the folder you are existing
from datetime import datetime, timezone


class User(db.Model): 
    id = db.Column(db.Integer(),primary_key = True)
    fullname = db.Column(db.String(),nullable = False)
    email = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    pincode = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(),default = "general")



class Parkinglot(db.Model):
    
    lotid = db.Column(db.Integer(),primary_key = True)
    location = db.Column(db.String(),nullable = False)
    address = db.Column(db.String(), nullable=False)
    pincode = db.Column(db.Integer(), nullable=False)
    total_slots = db.Column(db.Integer(), nullable=False)
    price_per_hour = db.Column(db.Float(), nullable=False)

    # for parent child relation
    # parkinglot_id = db.Column(db.Integer(),db.ForeignKey("parkinglot.id"),nullable = False)
    # to establish relationship add in Parkinglot Class - details = db.relationship("other table name",backref = "creator")
    spots = db.relationship(
    "Parkingspot",
    backref="parkinglot",
    cascade="all, delete-orphan")


class Parkingspot(db.Model):
    spot_id = db.Column(db.Integer, primary_key=True)
    lotid = db.Column(db.Integer, db.ForeignKey('parkinglot.lotid'), nullable=False)
    spot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('available', 'occupied', 'released', name='spot_status_enum'), default='available')
    vehicle_No = db.Column(db.String(20), nullable=True)
    parked_at = db.Column(db.DateTime, nullable=True)
    released_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship("User", backref="parked_spots")

    # parkinglot = db.relationship("Parkinglot", backref="spots")


