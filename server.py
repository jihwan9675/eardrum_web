# Writer = newjihwan
# lastest = 21.01.22. 22:17
# Composition[Front, Backend, DB]
# server.py is Backend. I also have DeepLearning(MASKRCNN+classification) Server(./deeplearningServer.py)
from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename
from pathlib import Path
from modules.dynamodb import dynamoDBsignin, dynamoDBcheckLogin, makemd5
import os, csv, cv2, sys, numpy, h5py, time, skimage.draw, datetime, socket, hashlib, multiprocessing, deeplearningServer

app = Flask(__name__) 

# Output List
eardrum = ["Normal","Traumatic Perforation", "Acute Otitis Media", "Chronic Otitis Media",
            "Congential Cholesteatoma", "Otitis Media with Effusion", "I don't know"]

# http://host:port/
# ex) http://0.0.0.0:80/ '0.0.0.0' = My IP
host = '0.0.0.0'  
port = "80"

# First page (./templates/index.html)
@app.route('/')
def index(): 
    return render_template('index.html')

# Singup page (./templates/signup.html)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        sign_id = request.form['sign_id']
        sign_pwd = request.form['sign_pwd1']
        # Password -> md5
        after_password = makemd5(sign_pwd)

        # Put data in AWS DynamoDB
        if dynamoDBsignin(sign_id, after_password):
            return render_template('login.html')
    return render_template('signup.html')

# Login Page ... I have to add GraphQL code.
# Login page (./templates/login.html)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        value_id = request.form['login_id']
        value_pwd = request.form['login_pwd']
        after_password = makemd5(value_pwd)

        if dynamoDBcheckLogin(value_id, after_password):
            return render_template('upload.html')
    return render_template('login.html')

# Image upload page
# Save Image and Predict in this method.
# Image Upload page (./templates/upload.html)
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # Save image ... Filename rule is current time.
        now = time.localtime()
        imageName=str(now.tm_hour)+str(now.tm_min)+str(now.tm_sec)+str(".jpg") 
        f = request.files['file']
        f.save("./static/uploader/"+imageName)
        print("Saved File : "+"./static/uploader/"+imageName)

        packet = sendPacket(imageName)

        # Packet Analaysis(String -> List)
        # ex) '1 2 99.5555' -> ['1', '2', '99.5555']
        # Index 0 : Detected Object's Count
        # Index 1 : Disease Index for List eardrum(Line 15)
        # Index 2 : Accuracy
        detectedCount_diseaseIndex_accuracy = packet.split(" ")
        print(detectedCount_diseaseIndex_accuracy)
        detectedCount = int(detectedCount_diseaseIndex_accuracy[0])
        disease = eardrum[int(detectedCount_diseaseIndex_accuracy[1])]
        acc = round(float(detectedCount_diseaseIndex_accuracy[2])*100,2)

        if detectedCount == 0:
            return render_template('cannotfind.html', name=imageName)
        return render_template('result.html', name=imageName, disease=disease, acc=acc)

def sendPacket(imageName):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # DeepLearning Server's Host, Port
    Deep_HOST = '127.0.0.1'  
    Deep_PORT = 9999
    client_socket.connect((Deep_HOST, Deep_PORT))
    client_socket.sendall(imageName.encode())

    # Receive predicted result from DeepLearning Server
    data = client_socket.recv(64)
    print('Received', repr(data.decode()))
    client_socket.close()

    return str(data.decode())

if __name__=='__main__':
    import multiprocessing
    import deeplearningServer
    proc = multiprocessing.Process(target=deeplearningServer.main) 
    proc.daemon=True
    proc.start()
    app.run(host=host, port=port, debug=True)
    
