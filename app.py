import os
from flask import Flask, render_template, request, redirect
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

    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

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

@app.route('/admin/upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
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

        return redirect('/gallery')
    else:
        return render_template('admin/upload_image.html')

@app.route('/admin/image')
def admin_images():
    data = db.session.query(Image).all()
    return render_template('admin/image.html', data=data)

@app.route('/admin/image/<int:id>', methods=['GET', 'POST'])
def admin_image(id):
    if request.method == 'POST':
        image = Image.query.get(id)
        db.session.delete(image)
        db.session.commit()
        return redirect('/admin/image')
    else:
        return redirect('/admin/image')

@app.route('/admin/album_upload', methods=['GET', 'POST'])
def admin_album():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        album = Album(name=request.form.get('name'), description=request.form.get('description'))
        for file in request.files.getlist('inputFile'):
            print(file)
            filename = file.filename
            destination = '/'.join([target, filename])
            print(destination)
            newFile = Image(name=file.filename, url='/static/images/' + filename, description="")
            album.gallery_image.append(newFile)
            file.save(destination)
        db.session.add(album)
        db.session.commit()

        return redirect('/gallery')
    else:
        return render_template('admin/upload_album.html')

@app.route('/admin/album')
def admin_albums():
    data = db.session.query(Album).all()
    new_data = []
    for item in data:
        tmp = {}
        tmp['id'] = item.id
        tmp['name'] = item.name
        tmp['description'] = item.description
        tmp['count'] = len(item.gallery_image)
        new_data.append(tmp)
        
    return render_template('admin/album.html', data=new_data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900, debug=True)
