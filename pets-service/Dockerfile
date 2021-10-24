FROM python:3.8-slim-buster
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV host_api=94.26.229.140
ENV port_api=5000
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt install -y libgl1-mesa-glx
RUN apt-get -y install tesseract-ocr
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
