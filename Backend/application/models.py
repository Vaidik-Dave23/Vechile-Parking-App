from application.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Parkinglot(db.Model):
    __tablename__ = 'parkinglots'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan')

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    parkinglot_id = db.Column(db.Integer, db.ForeignKey('parkinglots.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    parking_spot = db.relationship('ParkingSpot', backref=db.backref('reservations', lazy=True))