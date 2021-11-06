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

def draw_box(image, pred_info):
    image = cv2.rectangle(image,(int(pred_info['xmin']),int(pred_info['ymin']), int(pred_info['xmax']),int(pred_info['ymax'])),(255,255,0), 2)
    return image

def addres(max_count, results, df):
    address = []
    id = []
    district = []
    for i in range(0, len(results["text"])):
        text = results["text"][i]
        if '_' in text and len(text) > 2:
            for i in range(len(df['ID'])):
                if Levenshtein.distance(text, df['ID'][i]) <= max_count:
                    address.append(df['Address'][i])
                    id.append(df['ID'][i])
                    district.append(df['District'][i])
                else:
                    pass
        else:
            pass
    try:
        all_address = Counter(address)
        one_address = (max(all_address, key=all_address.get))
        all_id = Counter(id)
        one_id = (max(all_id, key=all_id.get))
        all_district = Counter(district)
        one_district = (max(all_district, key=all_district.get))
        return one_address, one_id, one_district
    except:
        return ''

def main_get_address(photos):
    df = pd.read_csv(f'service/static/addres_csv.csv')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    param = {'long': 2, 'short': 1, 'dark': 1, 'white': 2,
             'multi-color': 3, False: 0, True: 1}
    apps_color, apps_tail = int(db.session.query(Application).first().color), int(db.session.query(Application).first().tail)
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
                    db.session.add(Photos(id_application=1, filename=photo, is_animal_there=0, is_it_a_dog=0, is_the_owner=0, color=0, tail=0, result=result, cam_id='', address=''))
                else:
                    db.session.add(Photos(id_application=1, filename=photo, is_the_owner=param[predict.json()['master']], tail=param[predict.json()['tail']],is_animal_there=1, is_it_a_dog=1, cam_id='', address='', color=param[predict.json()['color']], result=result))
                    photo_draw = draw_box(image, predict.json()['pred_info'])
                    cv2.imwrite(f'service/uploads/{photo}', photo_draw)
            else:
                if predict.text == 'Dogs not found! :(':
                    db.session.add(Photos(id_application=1, filename=photo,district=res[2], address=re.sub(r'[^\w\s]','', res[0]).lower(),is_animal_there=0, color=0, tail=0, is_it_a_dog=0, is_the_owner=0, cam_id=res[1], result=result))
                else:
                    db.session.add(
                        Photos(id_application=1, filename=photo, district=res[2], is_the_owner=param[predict.json()['master']], is_it_a_dog=1, address=re.sub(r'[^\w\s]','', res[0]).lower(), cam_id=res[1], tail=param[predict.json()['tail']], is_animal_there=1,
                               color=param[predict.json()['color']], result=result))
                    photo_draw = draw_box(image, predict.json()['pred_info'])
                    cv2.imwrite(f'service/uploads/{photo}', photo_draw)
            db.session.commit()
        db.session.query(Application).filter_by(id=1).update({Application.status: 1})
        db.session.commit()

        data = db.session.query(Photos).all()

        df_result = pd.DataFrame([(d.filename, d.is_animal_there, d.is_it_a_dog, d.is_the_owner, d.color, d.tail, d.address, d.cam_id) for d in data],
            columns=['filename', 'is_animal_there', 'is_it_a_dog', 'is_the_owner_there', 'color', 'tail', 'address','cam_id'])

        df_result.to_csv('service/static/result.csv', encoding='cp1251')



