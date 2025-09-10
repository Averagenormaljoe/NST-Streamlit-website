
import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image
from keras.layers import TFSMLayer

def apply_model(img,style_model, show_image : bool =True):
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

def simple_style_transfer(image_path : str, model):
    if model is None:
        return None
    open_image = Image.open(image_path)
    if open_image is None:
        return None
    styled_image = style_transfer(open_image, model)
    if styled_image  is None:
        raise ValueError("Styled_image is none.")
    return styled_image


