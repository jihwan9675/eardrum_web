import os
from mrcnn.config import Config

os.environ['CUDA_DEVICE_ORDER']="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES']="0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class CustomConfig(Config):
    NAME = "eardrum"
    IMAGES_PER_GPU = 2
    NUM_CLASSES = 1 + 1
    STEPS_PER_EPOCH = 1000
    DETECTION_MIN_CONFIDENCE = 0.9

class InferenceConfig(CustomConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
