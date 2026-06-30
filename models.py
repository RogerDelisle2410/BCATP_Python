from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from datetime import datetime

class Bcatp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Army(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Airforce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Navy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Dewline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Pinetree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Defunct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Midcanada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Planes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Ships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class Tanks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    comment = db.Column(db.String(500))
    wiki = db.Column(db.String(500))

class VisitorCount(db.Model):
    __tablename__ = "VisitorCount"

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    last_visit = db.Column(db.DateTime)
    last_ip = db.Column(db.String(50))
    last_user_agent = db.Column(db.String(400))
    today_visits = db.Column(db.Integer, default=0)

class VisitorLog(db.Model):
    __tablename__ = "VisitorLog"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(100))
    user_agent = db.Column(db.String(500))
    is_owner = db.Column(db.Integer)  # 0 or 1
    location = db.Column(db.String(200))  # NEW: "Calgary, Canada"

