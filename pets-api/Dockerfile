FROM python:3.6-slim-buster

RUN pip install flask
RUN pip install requests
RUN pip install black
RUN pip install matplotlib>=3.2.2
RUN pip install numpy>=1.18.5
RUN pip install opencv-python>=4.1.2
RUN pip install Pillow
RUN pip install PyYAML>=5.3.1
RUN pip install scipy>=1.4.1
RUN pip install torch
RUN pip install torchvision
RUN pip install tqdm>=4.41.0
RUN pip install isr==2.2.0
RUN pip install tensorboard>=2.4.1
RUN pip install pytesseract
RUN pip install seaborn>=0.11.0
RUN pip install pandas
RUN pip install tensorflow
RUN pip install keras
RUN pip install thop

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
RUN pip install h5py==2.10.0
COPY . /app

EXPOSE 5000

CMD ["python", "webapp.py", "--port=5000"]