FROM python:3.7.9
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install libgl1-mesa-glx -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python","server.py","&" ]
