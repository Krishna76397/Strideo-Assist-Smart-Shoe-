# Image recognition example using VGG16 (from PDF)
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
import numpy as np
import cv2, os

model = None
def load_model():
    global model
    if model is None:
        model = VGG16(weights='imagenet')
    return model

def predict_image(img_path, top=3):
    if not os.path.exists(img_path):
        raise FileNotFoundError(img_path)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224,224))
    x = np.expand_dims(img, axis=0)
    x = preprocess_input(x)
    model = load_model()
    preds = model.predict(x)
    decoded = decode_predictions(preds, top=top)[0]
    return [(label, float(score)) for (_, label, score) in decoded]
