from .. import db

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    url = db.Column(db.String(300))
    price = db.Column(db.Integer,default=0)

    album = db.relationship("Album", back_populates="children")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))