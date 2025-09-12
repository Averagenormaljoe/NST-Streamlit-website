import os
import traceback
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

def get_AdaIN_model(model_path: str,size : tuple[int,int]):
    content_input = tf.keras.Input(shape=(size[0], size[1], 3))
    style_input = tf.keras.Input(shape=(size[0], size[1], 3))

    outputs = TFSMLayer(model_path)((content_input, style_input))
    inputs = [content_input, style_input]
    model = tf.keras.Model(inputs=inputs, outputs=outputs) 
    return model    

def get_forward_feed_model(model_path: str,size: tuple[int,int]):
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

def get_model_from_path(style_model_path : str,size : tuple[int,int] = (224, 224)):
    try:
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
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'get_model_from_path': {e}"
        print(mes)  
        st.error(mes)
    return model