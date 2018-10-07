import os, hashlib, shutil
from flask import Flask, render_template, request, redirect

from main.model.image import Image
from main.model.album import Album
from main.model.post import Post
from main.model.user import User

from main import app, db

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = b'ba1db3e47439b1365fd60f0335ad22e3'

@app.route('/', methods=['GET','POST'])
def index():
    wrong_username = None
    wrong_password = None
    if request.method == 'POST':
        atempt_usr = request.form.get('usrname')
        atempt_pwd = hashlib.sha256(request.form.get('pwd').encode()).hexdigest()
        data = db.session.query(User).all()
        for user in data:
            if atempt_usr == user.username:
                print('USR OK')
            elif not atempt_usr == user.username:
                wrong_username = True
                return render_template('index.html', wrong_username=wrong_username)
            if atempt_pwd == user.password:
                    print('PWD OK')
                    return redirect('/admin/post')
            elif not atempt_pwd == user.password:
                    wrong_password = True
                    return render_template('index.html', wrong_password=wrong_password)
            else: 
                return render_template('index.html')
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/blog')
def blog():
    data = db.session.query(Post).all()
    return render_template('blog.html', data=data)

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
        alb_name = request.form.get('name')
        target = os.path.join(APP_ROOT, 'main/static/images/' + alb_name + '/')
        if not os.path.isdir(target):
            os.mkdir(target)

        album = Album(name=alb_name, description=request.form.get('description'))
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

@app.route('/admin/album', methods=['GET','POST'])
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
        album = Album.query.get(id)
        target = os.path.join(APP_ROOT, 'main/static/images/' + album.name + '/')
        alb_images = Image.query.get(album.gallery_image).all()
        images = Image.query.get(id).all()
        db.session.delete(images)
                
        db.session.commit()
        shutil.rmtree(target)
        return redirect('/admin/album')
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
