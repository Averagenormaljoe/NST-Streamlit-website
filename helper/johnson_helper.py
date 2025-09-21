
import time
import numpy as np
import tensorflow as tf
from helper.style_transfer import resize_image
import streamlit as st
from PIL import Image
import cv2




def apply_model(img,style_model, output_size = (256,256), show_duration: bool = False):
    if style_model is None:
        raise ValueError("Failed to load model.")
    if img is None:
        st.error("apply_model:: image is none or invalid.")
        return None
    if style_model is None:
        st.error("apply_model:: style_model is none or invalid")
        return  None
    style_model.trainable = False
    try:
        x = (512, 512)
        resized_img = cv2.resize(img,x, interpolation=cv2.INTER_LINEAR)
        test_image = np.expand_dims(resized_img, axis=0)
        cast_img = test_image.astype(np.float32) 
        print("cast_img:", cast_img.shape)
        print("model shape:", style_model.input_shape)
        start_time = time.perf_counter()
        predicted_img = style_model(cast_img)
        end_time = time.perf_counter()
        duration : float = end_time - start_time
        print("Process time took:", f"{duration} for {x[0]}x{x[1]}" )
        if show_duration:
            st.success(f"Process time took: {duration} seconds for resolution {x[0]}x{x[1]}.")
        output = list(predicted_img.values())[0]
        clip_predicted_img = np.clip(output, 0, 255)
        output = clip_predicted_img.astype(np.uint8)
        test_output = tf.squeeze(output).numpy()
        return test_output
    except Exception as e:
        print(f"Error for 'apply_model': {e}")
    return None
 

def style_transfer(image, model,resize=True,  show_duration: bool = False):
    if model is None:
        st.error("Model not loaded. Please select a valid model.")
        return None

    try:
        print(f"Image shape prior to resizing: {image.shape}")
        content_numpy_image = resize_image(image, "Content Image") if resize else image
        print("content_numpy_image_shape:", content_numpy_image.shape)
        output = apply_model(content_numpy_image, model,show_duration=show_duration)
        return output
    except Exception as e:
        print(f"Error for 'style_transfer': {e}")
    return None

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


