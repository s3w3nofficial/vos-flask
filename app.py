import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    url = db.Column(db.String(300))

    voting_id = db.Column(db.Integer, db.ForeignKey('album.id'))

class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    description = db.Column(db.String(3000))

    gallery_image = db.relationship('Image', backref='album', lazy=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    data = db.session.query(Image).all()
    return render_template('gallery.html', data=data)

@app.route('/gallery/<int:id>')
def image(id):
    img = Image.query.get(id)
    return render_template('image.html', data=img)

@app.route('/admin/upload')
def admin_upload():
    return render_template('admin/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('inputFile'):
        print(file)
        filename = file.filename
        destination = '/'.join([target, filename])
        print(destination)
        newFile = Image(name=file.filename, url='/static/images/' + filename, description="")
        db.session.add(newFile)
        file.save(destination)

    db.session.commit()

    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900, debug=True)
