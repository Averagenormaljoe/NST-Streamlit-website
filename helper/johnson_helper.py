from importlib import simple
from operator import contains
import os
from pyexpat import model

import keras
import imutils
import cv2
import numpy as np
from cv2.typing import MatLike
import tensorflow_hub as hub
import tensorflow as tf
import streamlit as st
import PIL
from PIL import Image
from keras.layers import TFSMLayer
def create_model_from_endpoint(model_path: str):
    layer = TFSMLayer(model_path, call_endpoint="serving_default")

    model = keras.Sequential([
        keras.Input(shape=(256, 256, 3)), 
        layer
    ])
    return model
def get_model_from_path(style_model_path):
    if style_model_path.endswith('.t7') or style_model_path.endswith('.pth'):
        model = cv2.dnn.readNetFromTorch(style_model_path)
    elif style_model_path.endswith('.pb') or style_model_path.endswith('.pbtxt'):
        model = cv2.dnn.readNetFromTensorflow(style_model_path)
    elif "tfhub" in style_model_path:
        model = hub.load(style_model_path)
    elif style_model_path.endswith('.keras'):
        model = tf.keras.models.load_model(style_model_path)
    elif "forward_feed" in style_model_path:
        model = create_model_from_endpoint(style_model_path)
    else:
        st.error(f"This model path is invalid: {style_model_path}")
        return None
    return model

def style_transfer(image, model):
    if model is None:
        st.error("Model not loaded. Please select a valid model.")
        return None
    (h, w)  = image.shape[:2]
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #PIL Jpeg to Opencv image

    mean : tuple[float,float,float] = (103.939, 116.779, 123.680)
    
    blob : MatLike = cv2.dnn.blobFromImage(image, 1.0, (w, h), mean, swapRB=False, crop=False)
    model.setInput(blob)
    output = model.forward()

    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += mean[0]
    output[1] += mean[1]
    output[2] += mean[2]
    output /= 255.0
    output = output.transpose(1, 2, 0)
    output = np.clip(output, 0.0, 1.0)
    width : int = 500
    output = imutils.resize(output, width=width)
    return output

def simple_style_transfer(image_str, model):
    if model is None:
        return None
    open_image = Image.open(image_str)
    styled_image = style_transfer(open_image, model)
    return styled_image


