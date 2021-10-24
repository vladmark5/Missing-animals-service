import time

from pytesseract import Output
import pytesseract
import cv2
import pandas as pd
import Levenshtein
from collections import Counter
from service.models import db, Photos, Application
import re
from service.bcnn import image_predict

def addres(max_count, results, df):
    distrs = []
    id = []
    for i in range(0, len(results["text"])):
        text = results["text"][i]
        if '_' in text and len(text) > 2:
            for i in range(len(df['ID'])):
                if Levenshtein.distance(text, df['ID'][i]) <= max_count:
                    distrs.append(df['Address'][i])
                    id.append(df['ID'][i])
                else:
                    pass
        else:
            pass
    try:
        all_address = Counter(distrs)
        one_address = (max(all_address, key=all_address.get))
        all_id = Counter(id)
        one_id = (max(all_id, key=all_id.get))
        return one_address, one_id
    except:
        return ''

def main_get_address(photos):
    start = time.time()
    df = pd.read_csv(f'service/static/addres_csv.csv')
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    param = {'long': 'Длинный', 'short': 'Короткий/Нет хвоста', 'dark': 'Темный', 'white': 'Светлый',
             'multi-color': 'Светлый'}
    apps_color, apps_tail = db.session.query(Application).first().color, db.session.query(Application).first().tail
    for photo in photos:
        image = cv2.imread(f'service/uploads/{photo}')
        if image is None:
            pass
        else:
            thr = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]

            results = pytesseract.image_to_data(thr, output_type=Output.DICT)
            for i in range(3):
                res = addres(i, results, df)
                if len(res) > 0:
                    break
            predict = image_predict(image)
            try:
                result = 1 if param[predict.json()['tail']] == apps_tail and param[predict.json()['color']] == apps_color else 0
            except:
                result = 0
            if len(res) == 0:
                if predict.text == 'Dogs not found! :(':
                    db.session.add(Photos(id_application=1, filename=photo, is_animal_there=0, result=result))
                else:
                    db.session.add(Photos(id_application=1, filename=photo, tail=param[predict.json()['tail']],is_animal_there=1, color=param[predict.json()['color']], result=result))
            else:
                if predict.text == 'Dogs not found! :(':
                    db.session.add(Photos(id_application=1, filename=photo, address=re.sub(r'[^\w\s]','', res[0]).lower(),is_animal_there=0, cam_id=res[1], result=result))
                else:
                    db.session.add(
                        Photos(id_application=1, filename=photo, address=re.sub(r'[^\w\s]','', res[0]).lower(), cam_id=res[1], tail=param[predict.json()['tail']], is_animal_there=1,
                               color=param[predict.json()['color']], result=result))
            db.session.commit()
        db.session.query(Application).filter_by(id=1).update({Application.status: 1})
        db.session.commit()

        data = db.session.query(Photos).all()

        df_result = pd.DataFrame([(d.filename, d.is_animal_there, d.is_it_a_dog, d.is_the_owner, d.color, d.tail, d.address, d.cam_id) for d in data],
            columns=['filename', 'is_animal_there', 'is_it_a_dog', 'is_the_owner', 'color', 'tail', 'address','cam_id'])

        df_result.to_csv('service/static/result.csv', encoding='cp1251')



