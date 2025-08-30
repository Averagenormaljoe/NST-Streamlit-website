import os
import keras
from helper.model_validation import is_AdaIN, variables_dir_exists
import cv2
import numpy as np
from cv2.typing import MatLike
import tensorflow_hub as hub
import tensorflow as tf
import streamlit as st
from PIL import Image
from keras.layers import TFSMLayer

def get_AdaIN_model(model_path: str,size : tuple):
    content_input = tf.keras.Input(shape=(size[0], size[1], 3))
    style_input = tf.keras.Input(shape=(size[0], size[1], 3))

    outputs = TFSMLayer(model_path)((content_input, style_input))
    inputs = [content_input, style_input]
    model = tf.keras.Model(inputs=inputs, outputs=outputs) 
    return model    

def get_forward_feed_model(model_path: str,size: tuple):
    layer = TFSMLayer(model_path, call_endpoint="serving_default")

    model = keras.Sequential([
        keras.Input(shape=(size[0], size[1], 3)), 
        layer
    ])
    return model

def create_model_from_endpoint(model_path: str,size : tuple):
    
    if is_AdaIN(model_path):
        model = get_AdaIN_model(model_path, size)
        return model    
    forward_feed_size = (256,256)
    model = get_forward_feed_model(model_path,forward_feed_size)
    return model

def get_model_from_path(style_model_path,size = (224, 224)):
    if style_model_path is None or not isinstance(style_model_path,str):
        st.error("get_model_from_path:: error: model path is not a string or is none.")
        return None
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
    if img is None:
        st.error("apply_model:: image is none or invalid.")
        return
    if style_model is None:
        st.error("apply_model:: style_model is none or invalid")
        return 
    test_image = np.expand_dims(img, axis=0)
    converted_image = test_image / 255.0
    cast_img = converted_image.astype(np.float32)
    predicted_img = style_model(cast_img)
    output = list(predicted_img.values())[0]
    clip_predicted_img = np.clip(output, 0, 255)
    int8_predicted_img = clip_predicted_img.astype(np.uint8)
    output =  int8_predicted_img.astype(np.uint8)
    test_output = tf.squeeze(output).numpy()
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


