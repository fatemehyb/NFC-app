FROM python:3.8.16-buster 
WORKDIR /app 
COPY requirements.txt /app/ 
COPY NFC.py /app/ 
COPY templates /app/templates 
COPY static /app/static
RUN pip install -r requirements.txt 
# Install Mesa libraries 
RUN apt-get update && \ 
apt-get install -y libgl1-mesa-glx 
RUN apt-get update -y && apt-get install -y build-essential cmake \ 
libsm6 libxext6 libxrender-dev \ 
python3 python3-pip python3-dev 
EXPOSE 9003 
ENV DISPLAY=:0 
ENTRYPOINT ["python"] 
CMD ["NFC.py"] 
#run using this: 
#docker build -t my_python_app . 
#docker run --device /dev/video0:/Applications/IriunWebcam.app/Contents/MacOS/IriunWebcam -p 9003:9003 my_python_app 
#docker run -d --name cam --device /dev/video0 -p 9003:9003 my_python_app 