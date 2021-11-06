import argparse
import io
import os
import torch
from flask import Flask, render_template, request, redirect
import cv2
import json
import csv
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from tensorflow import keras 
import tensorflow as tf
import glob

def dog_detection(model,image):
    '''
    Input:
    model [:torchmodel] - загруженная модель нейронной сети
    image [:array] - изображение
    
    Output:
    results [:list] - список найденных объектов с координами и вероятностями
    '''
    
    results = model(image)
    results = results.pandas().xyxy[0].to_json(orient="records")
    results = json.loads(results)
    
    return results

def dog_cropping(image,result):
    '''
    Input:
    results [:list] - список найденных объектов с координами и вероятностями (один объект)
    image [:array] - изображение
    
    Output:
    cropping_dog [:array] - вырезанное изображение с собакой
    '''
    
    cropping_dog = image[int(result["ymin"]):int(result["ymax"]),int(result["xmin"]):int(result["xmax"])]
    
    return cropping_dog

def color_predict(model,image):
    '''
    Input:
    model [:tfmodel] -  загруженная модель нейронной сети классификации цвета собаки
    image [:array] - изображение
    
    Output:
    color [:str] - цвет собаки
    '''  
    
    colors_names = {"0":"multi-color",
                    "1":"dark",
                    "2":"white"}

    image_resize = cv2.resize(image, (60, 70))
    image_reshape = image_resize.reshape(1, 60, 70, 3) / 255
    prediction = model_color(image_reshape)
    color_idx = np.argmax(prediction, axis=1)
    color = colors_names[str(color_idx[0])]
    return color

def tail_predict(model,image):
    '''
    Input:
    model [:tfmodel] -  загруженная модель нейронной сети классификации длины хвоста собаки
    image [:array] - изображение
    
    Output:
    tail [:str] - длина хвоста собаки
    '''  
    
    tail_names = {"0":"long",
                    "1":"short",
                 "2":"short"}
    image_resize = cv2.resize(image, (60, 70))
    image_reshape = image_resize.reshape(1, 60, 70, 3) / 255
    prediction = model_tail(image_reshape)
    tail_idx = np.argmax(prediction, axis=1)
    tail = tail_names[str(tail_idx[0])]
    return tail
    
#Инициализируем приложение
app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello_world():
    return "Hello world!"

@app.route("/dog_detect", methods=["POST"])
def dog_detect():
    try:
        #Получаем запрос
        print("start.....")
        request_json = request.get_json(force=True)
        print("also start.....")
        #Выцепляем из него нужную нам дату
        images = request_json["images"]
        image_byte = images.encode()
        im_bytes = base64.b64decode(image_byte)   # im_bytes is a binary image
        im_file = BytesIO(im_bytes)  # convert image to file-like object
        img = Image.open(im_file)   # img is now PIL Image object
        img = np.asarray(img)
        
        dog_preds = dog_detection(model,img)
        print(dog_preds)
        dog_crop = dog_cropping(img,dog_preds[0])
        color = color_predict(model_color,dog_crop)
        tail = tail_predict(model_tail,dog_crop)

        retval, buffer = cv2.imencode('.jpg', dog_crop)
        base64_image = base64.b64encode(buffer)

        result = {'dog_image':base64_image.decode("utf-8"),
                'pred_info':dog_preds[0],
                'master':False,
                'tail':tail,
                'color':color}
        return result
    except:
        return "Dogs not found! :("

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    #Загружаем модели
    print("[INFO] Loading models ...")

    #Загружаем модель детектирования собак
    print("[INFO] Loading dog detection model ...")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.classes = 16
    print("[INFO] Model dog detection has been loaded!")
    
    #Загружаем модель классификации цвета
    print("[INFO] Loading color classifier model ...")
    model_color = tf.keras.models.load_model("./b-cnn_only_color_v1.1")
    print("[INFO] Model color classifier has been loaded!")

    #Загружаем модель классификации длины хвоста
    print("[INFO] Loading tail classifier model ...")
    model_tail = tf.keras.models.load_model("./b-cnn_only_tails_v1.2")
    print("[INFO] Model tail classifier has been loaded!")
    
    print("[INFO] Models has been loaded ...")
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
