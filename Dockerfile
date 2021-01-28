FROM python:3.7.9
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install libgl1-mesa-glx -y
RUN chmod 755 deeplearningServer.py
RUN chmod 755 server.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
ENTRYPOINT [ "nohup","python","deeplearningServer.py","&" ]
CMD [ "python","server.py","&" ]
