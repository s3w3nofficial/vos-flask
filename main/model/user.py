import hashlib, string, random
from .. import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    salt = db.Column(db.String(80), unique=True)

    def get_id(self):
        return self.id

    def __init__(self, username, password): 
        self.username = username
        self.salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        self.password = hashlib.sha256(password.encode() + self.salt.encode()).hexdigest()