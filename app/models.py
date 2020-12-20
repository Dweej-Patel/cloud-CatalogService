import enum
from app import db
from datetime import datetime


class EventType(enum.Enum):
    celebration = 0
    holiday = 1
    meeting = 2
    disco = 3
    culinary = 4
    other = 5


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(EventType), nullable=False, default=EventType.celebration)
    message = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event: '{self.id}', '{self.type}', '{self.created_date}', '{self.subject}', '{self.message}'"
