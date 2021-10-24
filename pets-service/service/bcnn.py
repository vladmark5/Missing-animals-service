import requests
import json
import cv2
import base64
import os



def image_predict(image):
    host = os.environ['host_api']
    port = os.environ['port_api']

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

