
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(100), unique=True, nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Room {self.room_number}>'
