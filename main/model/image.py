from .. import db

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    url = db.Column(db.String(300))

    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))