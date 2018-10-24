import os, hashlib, shutil
from flask import Flask, render_template, request, redirect, jsonify, flash, abort
from flask_login import LoginManager, login_user, login_required ,logout_user, UserMixin

from main.model.image import Image
from main.model.album import Album
from main.model.post import Post
from main.model.user import User

from main import app, db, login_manager

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = b'ba1db3e47439b1365fd60f0335ad22e3'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        print(request.json)
        atempt_usr = request.json.get("username")
        user = db.session.query(User).filter_by(username=atempt_usr).first()
        if not user == None:
            if not request.json.get("password") == None:
                atempt_pwd = hashlib.sha256(request.json.get("password").encode() + user.salt.encode()).hexdigest()
                if atempt_pwd == user.password:
                    login_user(user)
                    return jsonify({"status":"success"})
                else:
                    return jsonify({"status":"Chybně zadané heslo"})
            else:
                return jsonify({"status":"Something went wrong "})
        else:
            return jsonify({"status":"Chybně zadané jméno"})
    return abort(404)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/blog')
def blog():
    data = db.session.query(Post).all()
    return render_template('blog.html', data=data)

@app.route('/gallery')
def gallery():
    data = db.session.query(Album).all()
    return render_template('gallery.html', data=data)

@app.route('/gallery/<int:id>')
def image(id):
    img = Image.query.get(id)
    return render_template('image.html', data=img)

@app.route('/admin/upload', methods=['GET', 'POST'])
@login_required
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
        return abort(404)

@app.route('/admin/image')
@login_required
def admin_images():
    data = db.session.query(Image).all()
    return render_template('admin/images.html', data=data)

@app.route('/admin/image/<int:id>/a', methods=['GET', 'POST'])
@login_required
def admin_image_add(id):
    if request.method == 'POST':
        album = Album.query.get(id)
        target = os.path.join(APP_ROOT, 'main/static/images/' + album.name + '/')
        for file in request.files.getlist('inputFile'):
            print(file)
            filename = file.filename
            destination = '/'.join([target, filename])
            print(destination)
            newFile = Image(name=file.filename, url='/static/images/' + album.name + '/' + filename, description="")
            album.gallery_image.append(newFile)
            file.save(destination)
        db.session.commit()
        return redirect('/admin/album/{}'.format(album.id))
    return abort(404)


@app.route('/admin/image/<int:id>/d', methods=['GET', 'POST'])
@login_required
def admin_image_remove(id):
    if request.method == 'POST':
        image = Image.query.get(id)
        album = Album.query.get(image.album_id)
        target = os.path.join(APP_ROOT, 'main/static/images/' + album.name + '/' + image.name)
        db.session.delete(image)
        db.session.commit()
        os.remove(target)
        return redirect('/admin/album/{}'.format(image.album_id))
    else:
        return abort(404)

@app.route('/admin/album_upload', methods=['GET', 'POST'])
@login_required
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
            newFile = Image(name=file.filename, url='/static/images/' + alb_name + '/' + filename, description="")
            album.gallery_image.append(newFile)
            file.save(destination)
        db.session.add(album)
        db.session.commit()

        return redirect('/gallery')
    else:
        return render_template('admin/upload_album.html')

@app.route('/admin/album', methods=['GET','POST'])
@login_required
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

@app.route('/admin/album/<int:id>')
@login_required
def admin_album(id):
    data = Album.query.get(id)
    return render_template('admin/album.html', data=data)

@app.route('/admin/album/<int:id>/d', methods=['GET', 'POST'])
@login_required
def admin_album_remove(id):
    if request.method == 'POST':
        album = Album.query.get(id)
        alb_images = db.session.query(Image).filter_by(album_id=id).delete()
        db.session.delete(album)
        db.session.commit()
        target = os.path.join(APP_ROOT, 'main/static/images/' + album.name + '/')
        shutil.rmtree(target)
        return redirect('/admin/album')
    else:
        return abort(404)       

@app.route('/admin/posts')
@login_required
def admin_posts():
    data = db.session.query(Post).all()
    return render_template('admin/posts.html', data=data)

@app.route('/admin/post/<int:id>/d', methods=['GET', 'POST'])
@login_required
def admin_post_remove(id):
    if request.method == 'POST':
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/admin/posts')
    else:
        return abort(404)

@app.route('/admin/post/<int:id>',  methods=['GET', 'POST'])
@login_required
def admin_post_load(id):
    data = Post.query.get(id)
    if request.method == 'POST':
        return render_template('/admin/edit_post.html', data=data)
    else:
        return abort(404)

@app.route('/admin/post/<int:id>/e',  methods=['GET', 'POST'])
@login_required
def admin_post_edit(id):
    data = Post.query.get(id)
    if request.method == 'POST':
        data.name = request.form.get('name')
        data.content = request.form.get('content')
        db.session.commit()
        return redirect('/admin/posts')
    else:
        return abort(404)

@app.route('/admin/post_upload', methods=['GET', 'POST'])
@login_required
def admin_post_upload():
    if request.method == 'POST':
        post = Post(name=request.form.get('name'), content=request.form.get('content'))
        db.session.add(post)
        db.session.commit()
        return redirect('/admin/posts')
    else:
        return render_template('admin/upload_post.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5900, debug=True)
