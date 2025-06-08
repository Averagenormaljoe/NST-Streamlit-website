from tracemalloc import start
from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import av
from turn import get_ice_servers
from data import style_models_dict
from streamlit_session_memo import st_session_memo



def resize_image(input_image,name="Content Image"):
    size_threshold = (2000,2000)
    resizing_shape = (1000,1000)

    input_image_shape = input_image.shape
    
    resize_content = True if input_image_shape[0] > size_threshold[0] or input_image_shape[1] > size_threshold[1] else False
  
    if resize_content is True:
        print(f"{name} bigger than {size_threshold}, resizing to {resizing_shape}")
        input_image = cv2.resize(input_image,(resizing_shape[0],resizing_shape[1]))
        input_image = np.array(input_image)

    print(f"{name} Shape: ", input_image_shape)
    return input_image

def convert_to_numpy_image(image):
    return image.astype(np.float32)[np.newaxis, ...] / 255.
    

def transfer_style(content_image, style_image, hub_module):
    if style_image is None:
        return content_image
    print("Starting style transfer: ", style_image)

    content_image = resize_image(content_image, "Content Image")
    style_image = resize_image(style_image, "Style Image")

    # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1]. Example using numpy:
    content_image = convert_to_numpy_image(content_image)
    style_image = convert_to_numpy_image(style_image)

    # Optionally resize the images. It is recommended that the style image is about
    # 256 pixels (this size was used when training the style transfer network).
    # The content image can be any size.
    resize_style_shape = (256,256)
    style_image = tf.image.resize(style_image, resize_style_shape)

    print("Loading pre-trained model...")
    # The hub.load() loads any TF Hub model
    
    print("Generating stylized image now...wait a minute")
    # Stylize image.
    outputs = process_image(content_image, style_image, hub_module)
    
    stylized_image = get_stylized_image(outputs)
    return stylized_image

def process_image(content_image,style_image,hub_module):
    start_time = tf.timestamp()
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    end_time = tf.timestamp()
    processing_time : float = float(end_time - start_time)
    print(f"Stylizing completed in {processing_time:.2f} seconds...")
    return outputs
def get_stylized_image(outputs):
    output_image = outputs[0]
    # reshape the stylized image
    stylized_image = np.array(output_image)
    generated_image = stylized_image.reshape(
        stylized_image.shape[1], stylized_image.shape[2], stylized_image.shape[3])
    return generated_image