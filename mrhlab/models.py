from mrhlab.extensions import db
from datetime import datetime

class Pastebin(db.Model):
    shortlink = db.Column(db.String(10), primary_key=True)
    original = db.Column(db.String(255))
    paste_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)