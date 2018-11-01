from .. import db

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    street_address = db.Column(db.String(80))
    postal_code = db.Column(db.String(80))
    print_type = db.Column(db.String(80))

    order_images = db.relationship('Image', lazy=True, foreign_keys=[id])

    
