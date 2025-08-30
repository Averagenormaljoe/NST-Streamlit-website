import os
import keras
import imutils
import cv2
import numpy as np
from cv2.typing import MatLike
import tensorflow_hub as hub
import tensorflow as tf
import streamlit as st
from PIL import Image
from keras.layers import TFSMLayer
def create_model_from_endpoint(model_path: str,size : tuple):
    
    if "AdaIN" in model_path:
        input1 = tf.keras.Input(shape=(224, 224, 3))
        input2 = tf.keras.Input(shape=(224, 224, 3))

        output = TFSMLayer(model_path)((input1, input2))

        model = tf.keras.Model(inputs=[input1, input2], outputs=output) 
        return model    
    layer = TFSMLayer(model_path, call_endpoint="serving_default")

    model = keras.Sequential([
        keras.Input(shape=(256, 256, 3)), 
        layer
    ])
    return model
def variables_dir_exists(style_model_path: str) -> bool:
    return os.path.exists(os.path.join(style_model_path, "variables"))
def get_model_from_path(style_model_path,size = (256, 256)):
    if style_model_path.endswith('.t7') or style_model_path.endswith('.pth'):
        model = cv2.dnn.readNetFromTorch(style_model_path)
    elif style_model_path.endswith('.pb') or style_model_path.endswith('.pbtxt'):
        model = cv2.dnn.readNetFromTensorflow(style_model_path)
    elif "tfhub" in style_model_path:
        model = hub.load(style_model_path)
    elif style_model_path.endswith('.keras'):
        model = tf.keras.models.load_model(style_model_path)
    elif variables_dir_exists(style_model_path):
        model = create_model_from_endpoint(style_model_path,size)
    else:
        st.error(f"This model path is invalid: {style_model_path}")
        return None
    return model


def apply_model(img,style_model, show_image=True):
    test_image = np.expand_dims(img, axis=0)
    converted_image = test_image / 255.0
    cast_img = converted_image.astype(np.float32)
    predicted_img = style_model(cast_img)
    output = list(predicted_img.values())[0]
    clip_predicted_img = np.clip(output, 0, 255)
    int8_predicted_img = clip_predicted_img.astype(np.uint8)
    output =  int8_predicted_img.astype(np.uint8)
    test_output = tf.squeeze(output).numpy()
    predicted_output = tf.squeeze(int8_predicted_img).numpy()

    return test_output   

def style_transfer(image, model):
    if model is None:
        st.error("Model not loaded. Please select a valid model.")
        return None
    if  not hasattr(model, 'forward'):
        print(model.input_shape)
        (h, w) = (256, 256)
    else:
        (h, w)  = image.shape[:2]

    output = apply_model(image, model)
    
    return output

def simple_style_transfer(image_str, model):
    if model is None:
        return None
    open_image = Image.open(image_str)
    styled_image = style_transfer(open_image, model)
    return styled_image


