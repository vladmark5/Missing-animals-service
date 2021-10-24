import time

from service import app
from flask import render_template, request, send_from_directory, redirect, url_for
import json
from werkzeug.utils import secure_filename
from service.functions import allowed_file
import os
from service.models import db, Photos, Application
from service.address import main_get_address



@app.route('/')
@app.route('/main')
def main_page():
    if request.method == 'GET':
        apps = db.session.query(Application).first()
        return render_template('base.html', apps=apps)

@app.route('/about')
def about_page():
    if request.method == 'GET':
        apps = db.session.query(Application).first()
        return render_template('about.html', apps=apps)


@app.route('/create', methods=['GET', 'POST'])
def create():
    with open('service/static/district.json', 'rb') as file:
        j = json.load(file)
    districts = j['district']
    param = {'Светлый':0, 'Темный':1, 'Разноцветный':2, 'Длинный':0, 'Короткий/Нет хвоста':1}
    if request.method == 'GET':
        if len(db.session.query(Application).all()) != 0:
            return redirect(url_for('result'))
        else:
            return render_template('create.html', districts=districts)
    if request.method == 'POST':
        create = Application(animal='dog', photo=1, color=param[request.form.get('color')], tail=param[request.form.get('tils')])
        db.session.add(create)
        db.session.commit()
        files = request.files.getlist("file")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                pass
        # db.session.commit()
        main_get_address(os.listdir(app.config['UPLOAD_FOLDER']))
        # thr = Thread(target=main_get_address, args=[os.listdir(app.config['UPLOAD_FOLDER'])])
        # thr.start()
        return redirect(url_for('result'))


@app.route('/result', methods=["GET", 'POST'])
def result():
    files = db.session.query(Photos).all()
    if request.method == 'GET':
        apps = db.session.query(Application).first()
        if apps is None:
            return redirect(url_for('create'))
        else:
            return render_template('result.html', files=files, apps=apps)
    if request.method=='POST':
        for file in files:
            os.remove(f"service/uploads/{file.filename}")
        try:
            os.remove(f"service/static/result.csv")
        except:
            pass
        db.session.query(Application).delete()
        db.session.query(Photos).delete()
        db.session.commit()
        return redirect(url_for('create'))

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory('uploads', name)