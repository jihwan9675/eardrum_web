"""
last modify : 21.01.23
writer : newjihwan
This DeepLearning Server have two part that Mask R-CNN and Classification
MaskRCNN : Detect Eardrum
Classification ["Normal","Traumatic Perforation", "AOM", "COM", "Congential Cholesteatoma", "OME"]
jihwan9675@gmail.com
"""

import socket, os, sys, json, datetime, cv2, skimage.draw
import numpy as np
from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
from mrcnn import model as modellib, utils
from modules.CustomConfig import CustomConfig, InferenceConfig
from modules.preprocess import preprocess
from modules.build_model import build_model

# For Connected Flask Server
HOST = '127.0.0.1'   
PORT = 9999

directory = "../static/uploader/" # Image Save path

# Laod MASK R-CNN Model
config = InferenceConfig()
config.display()
model = modellib.MaskRCNN(mode="inference", config=config, model_dir="./logs")
model.load_weights("./Weight/mask_rcnn_eardrum_0043.h5", by_name=True)

# Load Classification Model
classificationModel = build_model(6)
classificationModel.load_weights("./Weight/efficientNetB0.h5")

def detect_roi(model, image_path=None):
    image = skimage.io.imread(directory+image_path)

    # Detect/Predict
    r = model.detect([image], verbose=1)[0]

    # No instance == dont need classification
    if r['rois'].shape[0] == 0: 
        return r['rois'].shape[0]

    # Detected Object's Range --> For Cropping
    y1, x1, y2, x2 = r['rois'][0] 
    crop_image=image[y1:y2,x1:x2]

    # Save Image include Detected information
    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                        "Ear", r['scores'], 
                        title="Predictions",filename=directory+"detected"+image_path)
    # Save Croped Image
    skimage.io.imsave(directory+"cropped"+image_path, crop_image)

    return r['rois'].shape[0]

def predictEardiease(image_path):
    # Preprocess : Resize and CLAHE
    img=preprocess(directory+"cropped"+image_path)

    # Predict
    prediction = classificationModel.predict(img, verbose=1)

    # Find Max value's Index
    max_value=max(prediction[0])
    print(max_value)
    idx = np.where(prediction[0]==max_value)[0][0]

    return idx, max_value

def main():
    while True:
        # Create Socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Avoid Error

        # (Host = 127.0.0.1 / Port = 9999) ---> Connected Flask Server
        server_socket.bind((HOST, PORT)) 
        server_socket.listen() # Wait

        # When get request
        client_socket, addr = server_socket.accept()
        print('Connected by', addr)
        data = client_socket.recv(64)

        # If get the request, it will detect Eardrum.
        result=detect_roi(model, image_path=data.decode())

        idx = 6
        max_value = 0
        if result > 0:
            idx, max_value = predictEardiease(data.decode())
        packet = str(result) + " " + str(idx) + " " + str(max_value)
        print(packet)

        # Send Detected Image FileName
        print('Received from', addr, data.decode())
        client_socket.sendall(packet.encode())

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
	try:
		main()
		sys.exit()
	except (EOFError, KeyboardInterrupt) as err:
		print("Keyboard Interupted or Error!!!")