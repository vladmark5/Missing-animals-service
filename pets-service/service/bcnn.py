# import numpy as np
# from PIL import Image
# from pytesseract import Output
# import pytesseract
# import cv2
# import pandas as pd
# import Levenshtein
# from collections import Counter
# import base64

# import os

# def addres(max_count, results, df):
#     distrs = []
#     id = []
#     for i in range(0, len(results["text"])):
#         text = results["text"][i].replace('.', '').replace(',', '')
#         print(text)
#         if '_' in text:
#             for i in range(len(df['ID'])):
#                 if Levenshtein.distance(text, df['ID'][i]) <= max_count:
#                     distrs.append(df['Address'][i])
#                     id.append(df['ID'][i])
#                 else:
#                     pass
#         else:
#             pass
#     print(distrs)
#     try:
#         all_address = Counter(distrs)
#         one_address = (max(all_address, key=all_address.get))
#         all_id = Counter(id)
#         one_id = (max(all_id, key=all_id.get))
#         print(one_address, one_id)
#         return one_address, one_id
#     except:
#         return ''
#
# def main_get_address(fiels):
#     final = []
#     df = pd.read_csv('static/addres_csv.csv')
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
#     for i in fiels:
#         img = cv2.imread(f'Q:/SFDP/service/uploads/{i}')
#         HSV_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         h, s, v = cv2.split(HSV_img)
#
#         thr = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
#         # thr = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]
#
#
#
#         results = pytesseract.image_to_data(thr, output_type=Output.DICT)
#         print(results)
#         for i in range(3):
#             res = addres(i, results, df)
#             if len(res) > 0:
#                 break
#         final.append(res)
#     return final
#
#
# f = os.listdir(f'Q:/SFDP/service/uploads/')


import requests
import json
import cv2
import base64




def image_predict(image):
    host = "94.26.229.140"
    port = "5000"

    retval, buffer = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(buffer)
    data = json.dumps({'images': base64_image.decode("utf-8")})
    """
    Функция предсказания грейда по фотоколлажу (через tensorflow serving)
    """
    # form JSON request
    headers = {"content-type": "application/json"}
    server_url = f'http://{host}:{port}/dog_detect'
    json_response = requests.post(server_url, data=data, headers=headers)
    # save predict to var
    return json_response

