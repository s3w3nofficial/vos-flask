import os
from flask import Flask, render_template, request, redirect

from main.model.image import Image
from main.model.album import Album
from main.model.post import Post

from main import app, db

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
def admin_image_upload():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'main/static/images/')
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
    return render_template('admin/images.html', data=data)

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
def admin_album_upload():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'main/static/images/')
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
        
    return render_template('admin/albums.html', data=new_data)

@app.route('/admin/album/<int:id>', methods=['GET', 'POST'])
def admin_album(id):
    if request.method == 'POST':
        pass
    else:
        data = Album.query.get(id)
        return render_template('admin/album.html', data=data)

@app.route('/admin/post')
def admin_posts():
    data = db.session.query(Post).all()
    return render_template('admin/posts.html', data=data)

@app.route('/admin/post_upload', methods=['GET', 'POST'])
def admin_post_upload():
    if request.method == 'POST':
        post = Post(name=request.form.get('name'), content=request.form.get('content'))
        db.session.add(post)
        db.session.commit()
        return redirect('/admin/post')
    else:
        return render_template('admin/upload_post.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900, debug=True)
