import time

from service import app
from flask import render_template, request, send_from_directory, redirect, url_for
import json
from werkzeug.utils import secure_filename
from service.functions import allowed_file
import os
from service.models import db, Photos, Application, Testphotos
from service.address import main_get_address
import pandas as pd


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
    foto_list = []
    test_photo = os.listdir(app.config['UPLOAD_FOLDER'])
    param = {'Светлый':2, 'Темный':0, 'Разноцветный':3, 'Длинный':2, 'Короткий/Нет хвоста':0}
    if request.method == 'GET':
        if len(db.session.query(Application).all()) != 0:
            return redirect(url_for('result'))
        else:
            return render_template('create.html', districts=districts)
    if request.method == 'POST':
        create = Application(animal='dog', photo=1, color=param[request.form.get('color')], tail=param[request.form.get('tils')], type=request.form['confirm'])
        db.session.add(create)
        db.session.commit()
        if request.form['confirm'] == "0":
            files = request.files.getlist("file")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    if filename in test_photo:
                        filename = '_' + filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    foto_list.append(filename)
            # db.session.commit()
            main_get_address(foto_list)
        else:
            db.session.query(Application).filter_by(id=1).update({Application.status: 1})
            db.session.commit()
        # thr = Thread(target=main_get_address, args=[os.listdir(app.config['UPLOAD_FOLDER'])])
        # thr.start()
        return redirect(url_for('result'))


@app.route('/result', methods=["GET", 'POST'])
def result():

    type = db.session.query(Application).filter_by(id=1).first()
    if request.method == 'GET':
        apps = db.session.query(Application).first()
        if apps is None:
            return redirect(url_for('create'))
        else:
            if type.type == 0:
                files = db.session.query(Photos).filter_by(result=1).all()
                return render_template('result.html', files=files, apps=apps)
            else:
                file_test = db.session.query(Testphotos).filter_by(color=type.color, tail=type.tail, is_it_a_dog=1).all()
                df_result = pd.DataFrame([(
                                          d.filename, d.is_animal_there, d.is_it_a_dog, d.is_the_owner, d.color, d.tail,
                                          d.address, d.cam_id) for d in file_test],
                                         columns=['filename', 'is_animal_there', 'is_it_a_dog', 'is_the_owner', 'color',
                                                  'tail', 'address', 'cam_id'])

                df_result.to_csv('service/static/result.csv', encoding='cp1251')
                return render_template('result.html', files=file_test, apps=apps)
    if request.method=='POST':
        if type.type == 0:
            files = db.session.query(Photos).all()
            for file in files:
                os.remove(f"service/uploads/{file.filename}")
            try:
                os.remove(f"service/static/result.csv")
            except:
                pass
        else:
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