import sys, os, numpy
from tensorflow.keras.applications import EfficientNetB0
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import optimizers, losses, metrics

def build_model(nb_classes):
    base_model = EfficientNetB0(weights='imagenet', include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(nb_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    for layer in base_model.layers:
        layer.trainable = True
    Adadelta0 = optimizers.Adadelta(lr=0.013)
    model.compile(optimizer=Adadelta0,loss='sparse_categorical_crossentropy',metrics=['sparse_categorical_accuracy'])
    #model.load_weights("./Weight/efficientNetB0.h5")
    return model
