import datetime
from .. import db

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    content = db.Column(db.String(3000))
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    gallery_image = db.relationship('Image', backref='post', lazy=True)
    album = db.relationship('Album', backref='post', lazy=True)