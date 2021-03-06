from .. import db

class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    
    gallery_image = db.relationship('Image', back_populates="parent", lazy=True)